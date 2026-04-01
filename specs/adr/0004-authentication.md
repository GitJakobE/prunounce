# ADR-0004: Authentication Strategy — Stateless JWT

- **Status:** Accepted
- **Date:** 2026-03-16
- **Deciders:** Development team
- **Requirements:** REQ-4 (User authentication), REQ-7 (Host persona persistence), REQ-10 (Data persistence)

## Context and Problem Statement

All application content is gated behind authentication (REQ-4). The system needs to authenticate API requests from the React SPA, persist sessions across browser restarts, support email/password and Google social login, and authorise access to audio files served via `<audio>` element `src` attributes (which cannot set HTTP headers).

## Decision Drivers

- Stateless API design — no server-side session store required
- SPA-compatible — token stored client-side, sent with every API request
- Must work with `<audio>` element `src` URLs (cannot set Authorization headers)
- Support for both email/password and Google OAuth login flows
- Simple implementation for a small-scale application
- Secure by default — tokens must expire, passwords must be hashed

## Considered Options

### Option 1: Stateless JWT with localStorage + query parameter fallback (Chosen)

Issue a signed JWT on login/registration. The frontend stores it in localStorage and sends it via the `Authorization: Bearer` header. For resources that can't set headers (e.g., `<audio src="...">`), the token is passed as a `?token=` query parameter. The auth middleware accepts both.

### Option 2: Server-side sessions with cookies

Traditional session-based auth with an HTTP-only cookie. Sessions are stored in a database or in-memory store (e.g., Redis). Cookies are sent automatically by the browser, solving the `<audio>` src problem natively. However, this requires a session store (added infrastructure), and CORS + SameSite cookie configuration adds complexity for the SPA ↔ API setup during development. Scaling beyond a single server node requires shared session storage.

### Option 3: JWT in HTTP-only cookies

Combines JWT's statelessness with cookie-based transport. The JWT is set as an HTTP-only, Secure, SameSite cookie. This avoids localStorage XSS risks and works for `<audio>` elements natively. However, CSRF protection becomes necessary, and the cookie-based approach adds complexity with the Vite dev proxy setup.

### Option 4: OAuth 2.0 with opaque access tokens

A more formal OAuth flow using opaque tokens validated against a token store. Provides better revocation capability. However, the implementation complexity is significant for a single-application use case with no third-party API consumers.

## Decision Outcome

**Chosen: Option 1 — Stateless JWT with localStorage + query parameter fallback**

### Consequences

**Positive:**
- No server-side session store — the JWT is self-contained and verified with a shared secret
- Simple implementation: `jsonwebtoken.sign()` on login, `jsonwebtoken.verify()` in middleware
- The query parameter fallback (`?token=`) cleanly solves the `<audio>` element constraint
- Google social login issues the same JWT format, unifying the auth flow
- bcryptjs hashes passwords with salt — passwords are never stored in plain text
- Token expiry (configured via `JWT_EXPIRES_IN`) provides automatic session timeout

**Negative:**
- JWTs in localStorage are accessible to XSS attacks — mitigated by Content Security Policy headers (helmet) and input sanitisation
- JWTs cannot be revoked before expiry without a server-side blocklist — acceptable for v1 given the low-risk profile (no financial data, no admin operations)
- Query parameter tokens appear in server access logs — mitigated by not logging query strings in production and using HTTPS
- Token size (~300 bytes) is larger than a session ID cookie

**Neutral:**
- The auth middleware checks `Authorization: Bearer <token>` first, then falls back to `req.query.token` — a single middleware handles both paths
- express-validator validates email format and password strength at the registration endpoint
- Google OAuth validation uses the Google `token_endpoint` to verify the credential server-side

### Security Measures

| Concern | Mitigation |
|---|---|
| Password storage | bcryptjs with automatic salt (cost factor 10) |
| XSS → token theft | helmet CSP headers, no `dangerouslySetInnerHTML` |
| Token in URL | HTTPS in production, access logs exclude query strings |
| Brute force login | Login rate limiting required (see auth FRD 3.8) — not yet implemented |
| Password complexity | express-validator enforces minimum strength at registration |
| GDPR compliance | Account deletion cascades to all user data via Prisma `onDelete: Cascade` |
| Email dependency | Password reset and email verification require an email delivery service (see auth FRD 3.10) — not yet implemented |
