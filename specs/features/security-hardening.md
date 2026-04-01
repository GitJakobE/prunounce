# Feature Requirements Document — Security Hardening

**Parent PRD:** [prd.md](../prd.md)
**Feature ID:** F-SEC
**Requirement:** REQ-17
**Priority:** P0 (Must-have for launch)

## 1. Overview

The application must ship with secure defaults that protect user data, prevent common web vulnerabilities, and ensure the system cannot accidentally run in an insecure configuration. This FRD captures the security controls that go beyond basic authentication (covered in F-AUTH) and are needed for production readiness.

## 2. User Stories

| ID | Story | Acceptance Criteria |
|---|---|---|
| US-SEC1 | As an operator, I want the application to refuse to start if critical secrets are missing, so I cannot accidentally deploy an insecure configuration. | Application fails to start with a clear error message when `JWT_SECRET` is not set or equals a known placeholder value. |
| US-SEC2 | As a user, I want my authentication token to be protected from accidental exposure, so my account cannot be hijacked via leaked URLs or logs. | Tokens are not included in URL query strings except where technically unavoidable (e.g., `<audio>` element sources). Where query-string tokens are used, they are short-lived or scoped. |
| US-SEC3 | As a user, I want my session to be renewed periodically, so that a stolen token has limited usefulness. | A refresh-token mechanism exists so that the primary access token is short-lived (suggested: ≤ 1 hour) while the user experience remains seamless (no forced re-login within 30 days). |
| US-SEC4 | As an operator, I want the system to reject abnormally large requests, so it is resilient to denial-of-service attempts via payload flooding. | All API endpoints enforce a maximum request body size (suggested: 1 MB). Requests exceeding the limit receive a 413 response. |
| US-SEC5 | As a user, I want the application to include modern security headers in every response, so my browser can enforce protections against XSS, clickjacking, and data sniffing. | Responses include at minimum: `Content-Security-Policy`, `Strict-Transport-Security`, `X-Content-Type-Options`, `X-Frame-Options`. |
| US-SEC6 | As an operator, I want to be alerted when dependencies have known vulnerabilities, so I can patch them before they are exploited. | An automated dependency audit runs in CI and flags any dependency with a known high or critical severity vulnerability. |

## 3. Functional Requirements

### 3.1 Mandatory Secret Validation

- The application must validate all required secrets at startup before accepting any requests.
- If `JWT_SECRET` is unset, empty, or set to a known default placeholder (e.g., `"change-me"`), the application must refuse to start and log a clear, actionable error message.
- This validation must apply to both backend implementations (Node.js and Python).

### 3.2 Token Exposure Minimisation

- Authentication tokens must not appear in URL query strings for standard API requests.
- Where tokens must appear in query strings for technical reasons (e.g., `<audio>` or `<img>` element `src` attributes that do not support custom headers), those tokens should be:
  - Short-lived (separate from the main session token), **or**
  - Scoped to the specific resource being accessed
- Server access logs must not record full tokens. If tokens appear in request URLs, operators should be advised to configure log redaction.

### 3.3 Token Lifecycle & Refresh

- The system must support a two-token model:
  - **Access token**: short-lived (suggested: ≤ 1 hour), used for API requests.
  - **Refresh token**: long-lived (suggested: 30 days), used only to obtain new access tokens.
- Expired access tokens must return 401; the client must automatically request a new access token using the refresh token without user interaction.
- Refresh tokens must be revocable (e.g., deleted on logout, rotated on use).
- The overall user experience must remain seamless — users should not need to re-login within the 30-day window unless they explicitly log out or their refresh token is revoked.

### 3.4 Request Size Limits

- All API endpoints must enforce a maximum request body size.
- Suggested default: 1 MB for JSON payloads.
- Requests exceeding the limit must be rejected with HTTP 413 (Payload Too Large) and a clear error message.
- This must apply to both backend implementations.

### 3.5 Security Response Headers

- Every HTTP response from the backend must include security-hardening headers.
- Required headers:
  - `Content-Security-Policy` — restricts sources for scripts, styles, media, and connections to trusted origins only.
  - `Strict-Transport-Security` — enforces HTTPS for all future requests (suggested: `max-age=31536000; includeSubDomains`).
  - `X-Content-Type-Options: nosniff` — prevents MIME-type sniffing.
  - `X-Frame-Options: DENY` — prevents the site from being embedded in iframes.
- Headers already provided by existing middleware (e.g., Helmet) count toward this requirement; this FRD does not mandate redundant implementation if the middleware is properly configured.

### 3.6 Content Security Policy

- The `Content-Security-Policy` header must be configured to:
  - Allow scripts only from the application's own origin (no inline scripts unless hashed/nonced).
  - Allow styles only from the application's own origin and any required CDN for fonts.
  - Allow media (audio) only from the application's own API origin.
  - Allow connections (fetch/XHR) only to the application's own API origin.
  - Block all other sources by default (`default-src 'none'`).
- The CSP must not break existing functionality. If inline scripts or styles are currently required, they must be refactored to external files or use nonces/hashes.

### 3.7 Automated Dependency Auditing

- The CI pipeline must include an automated step that checks for known vulnerabilities in project dependencies.
- Vulnerabilities rated High or Critical must cause the CI step to fail (or produce a visible warning, depending on team policy).
- This applies to both Node.js (`npm audit`) and Python (`pip audit` or equivalent) dependency trees.
- Suggested cadence: on every PR and on a weekly scheduled run.

### 3.8 HTTPS Enforcement

- In production, the application must redirect all HTTP requests to HTTPS.
- This may be enforced at the reverse proxy layer (e.g., nginx) rather than in application code, but it must be documented and verified.
- The `Strict-Transport-Security` header (see 3.5) provides defense-in-depth after the first HTTPS visit.

## 4. Edge Cases

- If the only remaining secret to validate is `JWT_SECRET` and it uses the default placeholder, the startup failure message must explicitly name the variable and explain what to do (e.g., "Set the JWT_SECRET environment variable to a random string of at least 32 characters").
- If a refresh token is used after being revoked (e.g., user logged out on another device), the response must be 401 and the client must redirect to login.
- If the CSP blocks a legitimate resource, the developer must be able to diagnose it via the browser console's CSP violation reports before adjusting the policy.

## 5. Acceptance Criteria

- [ ] Application refuses to start when `JWT_SECRET` is missing or set to a placeholder value, with a clear error message.
- [ ] Standard API requests do not include tokens in URL query strings.
- [ ] Audio/resource URLs that require query-string tokens use short-lived or scoped tokens.
- [ ] A refresh-token mechanism is implemented; access tokens expire within 1 hour.
- [ ] All API endpoints reject payloads larger than the configured maximum with HTTP 413.
- [ ] `Content-Security-Policy` header is present on all responses and restricts sources to trusted origins.
- [ ] `Strict-Transport-Security` header is present on all responses in production.
- [ ] `X-Content-Type-Options` and `X-Frame-Options` headers are present on all responses.
- [ ] CI pipeline includes automated dependency vulnerability checks for both Node.js and Python.
- [ ] HTTP-to-HTTPS redirection is documented and enforced in production.

## 6. Out of Scope

- Web Application Firewall (WAF) rules — infrastructure-level concern, not application layer.
- Penetration testing — important but a separate activity, not a feature requirement.
- Role-based access control / admin privileges — no admin role exists in the current product scope.
- Encryption at rest for the database file — deferred to infrastructure decisions.
