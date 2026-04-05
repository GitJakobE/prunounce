# ADR-0030: Token Lifecycle & Session Security

- **Status:** Proposed
- **Date:** 2026-04-05
- **Deciders:** Development team
- **Requirements:** REQ-4 (User authentication), REQ-17 (Security Hardening), F-SEC (Security Hardening), F-AUTH (User Authentication)
- **Extends:** [ADR-0004](0004-authentication.md) (Stateless JWT)
- **Related:** [ADR-0007](0007-audio-delivery.md) (Audio Delivery — token in query string)

## Context and Problem Statement

ADR-0004 established stateless JWT authentication with a single long-lived token stored in localStorage. The Security Hardening FRD (F-SEC) now requires a more robust token lifecycle:

1. **Two-token model** — A short-lived access token (≤ 1 hour) paired with a long-lived refresh token (30 days), so that a stolen access token has limited usefulness (US-SEC3).
2. **Token exposure minimisation** — Tokens in URL query strings (used for `<audio>` and `<img>` elements per ADR-0004/0007) should be short-lived or scoped (US-SEC2).
3. **Security response headers** — Every response must include CSP, HSTS, X-Content-Type-Options, and X-Frame-Options (US-SEC5).
4. **Request size limits** — All endpoints must reject payloads exceeding 1 MB (US-SEC4).
5. **Mandatory secret validation** — The app must refuse to start if `JWT_SECRET` is missing or set to a placeholder (US-SEC1).

ADR-0004 acknowledged that single-token JWT "cannot be revoked before expiry" as a known negative. The two-token model addresses this by making the access token short-lived and the refresh token revocable.

## Decision Drivers

- F-SEC requires the two-token model — this is a P0 launch requirement
- The existing `<audio src="...?token=">` pattern sends tokens in URLs that appear in logs; short-lived tokens limit the exposure window
- Refresh tokens must be revocable (on logout, password change, or compromise)
- The user experience must remain seamless — no forced re-login within 30 days
- Implementation must work with the existing FastAPI + SQLAlchemy backend and React SPA frontend
- SQLite must remain the sole datastore (no Redis or external session store)

## Considered Options

### Option 1: Short-lived access JWT + database-backed refresh token (Chosen)

**Access token:**
- Stateless JWT, signed with `JWT_SECRET`
- Expiry: 15 minutes
- Contains user ID, email, and issued-at timestamp
- Sent via `Authorization: Bearer` header for API requests
- Also accepted via `?token=` query parameter for `<audio>` / `<img>` elements (unchanged from ADR-0004)
- Short lifetime limits exposure if token is logged in server access logs via query string

**Refresh token:**
- Opaque random string (not a JWT), stored in a `RefreshToken` database table
- Expiry: 30 days
- Associated with a user ID
- Sent to a dedicated `POST /api/auth/refresh` endpoint to obtain a new access token
- Stored in the frontend in localStorage alongside the access token
- Revoked on logout (deleted from database) and rotated on each use (old token deleted, new one issued)

**Database table:**

```
RefreshToken
  id          INTEGER PRIMARY KEY
  user_id     INTEGER NOT NULL  -- FK to User
  token       TEXT NOT NULL UNIQUE  -- opaque random string (32 bytes, hex-encoded)
  expires_at  DATETIME NOT NULL
  created_at  DATETIME NOT NULL
```

### Option 2: Short-lived access JWT + refresh JWT (both stateless)

Use two JWTs: a short-lived access JWT and a long-lived refresh JWT. Both are stateless.

**Pros:**
- No database table needed for refresh tokens
- Consistent token format

**Cons:**
- **Refresh tokens cannot be revoked** — a stolen refresh JWT is valid for 30 days with no server-side mechanism to invalidate it
- Logout becomes cosmetic (frontend deletes the token, but it's still valid if someone captured it)
- Violates F-SEC's requirement that refresh tokens be revocable

### Option 3: Server-side sessions (replace JWT entirely)

Replace JWT with traditional server-side sessions stored in SQLite, using HTTP-only cookies.

**Pros:**
- Sessions are inherently revocable (delete the row)
- No token in localStorage — immune to XSS token theft
- Cookies work natively with `<audio>` elements — no query-string tokens needed

**Cons:**
- Major rewrite — conflicts with ADR-0004's stateless architecture
- Requires CSRF protection (tokens in forms/headers)
- Cookie configuration complexity (SameSite, Secure, domain) with the Vite dev proxy
- Every API request hits the database for session lookup (mitigated by caching, but adds latency)

### Option 4: Keep single long-lived JWT (status quo)

Make no changes. Accept the risks documented in ADR-0004.

**Pros:**
- No implementation effort

**Cons:**
- **Directly violates** F-SEC requirements (US-SEC3: short-lived access token, revocable refresh token)
- A stolen token is valid for its full lifetime (potentially days/weeks)
- No mechanism to force logout on password change or account compromise

## Decision Outcome

**Chosen: Option 1 — Short-lived access JWT + database-backed refresh token**

### Token Lifecycle Flow

```
1. Login (POST /api/auth/login)
   → Backend verifies credentials
   → Creates RefreshToken row (30-day expiry)
   → Signs access JWT (15-minute expiry)
   → Returns { accessToken, refreshToken, expiresIn }

2. API requests
   → Frontend sends accessToken via Authorization: Bearer header
   → Backend verifies JWT signature and expiry
   → If expired → 401 response

3. Token refresh (POST /api/auth/refresh)
   → Frontend sends { refreshToken }
   → Backend looks up RefreshToken in database
   → If valid and not expired:
     - Deletes the old RefreshToken row (rotation)
     - Creates a new RefreshToken row
     - Signs a new access JWT
     → Returns { accessToken, refreshToken, expiresIn }
   → If invalid or expired → 401 (forces re-login)

4. Logout (POST /api/auth/logout)
   → Backend deletes all RefreshToken rows for the user
   → Frontend clears both tokens from localStorage

5. Audio/image requests
   → <audio src="/api/audio/123?token={accessToken}">
   → 15-minute token limits exposure window in server logs
```

### Frontend Integration

The React SPA implements transparent token refresh:

1. An Axios/fetch interceptor detects 401 responses
2. If a refresh token exists, it calls `POST /api/auth/refresh`
3. On success, retries the original request with the new access token
4. On failure (refresh token expired/revoked), redirects to login
5. A mutex prevents concurrent refresh calls from multiple components

### Security Response Headers

Implemented via FastAPI middleware (or Starlette middleware):

```python
@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = (
        "default-src 'none'; "
        "script-src 'self'; "
        "style-src 'self' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self'; "
        "media-src 'self'; "
        "connect-src 'self'; "
        "frame-ancestors 'none'"
    )
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response
```

### Request Size Limits

```python
# FastAPI/Starlette request body limit
app = FastAPI()
app.add_middleware(
    TrustedHostMiddleware,  # existing
)
# Limit request body to 1 MB
@app.middleware("http")
async def limit_request_size(request, call_next):
    if request.headers.get("content-length"):
        if int(request.headers["content-length"]) > 1_048_576:
            return JSONResponse(status_code=413, content={"detail": "Request body too large"})
    return await call_next(request)
```

### Startup Secret Validation

```python
@app.on_event("startup")
def validate_secrets():
    jwt_secret = os.getenv("JWT_SECRET", "")
    blocked = {"", "change-me", "secret", "your-secret-here"}
    if jwt_secret in blocked:
        raise SystemExit("FATAL: JWT_SECRET is missing or set to a placeholder value. Set a strong secret before starting the application.")
```

### Refresh Token Cleanup

A background task or startup hook periodically deletes expired refresh tokens:

```python
# Run on startup and daily via a scheduled task
def cleanup_expired_tokens(db: Session):
    db.query(RefreshToken).filter(RefreshToken.expires_at < datetime.utcnow()).delete()
    db.commit()
```

## Consequences

**Positive:**
- Access tokens are short-lived (15 min) — stolen tokens have a narrow exploitation window
- Refresh tokens are revocable — logout, password change, and admin actions can force re-authentication
- Token rotation on refresh prevents replay attacks with old refresh tokens
- Security headers protect against XSS, clickjacking, and MIME sniffing
- Request size limits prevent payload-based denial of service
- Startup validation prevents insecure deployments
- `<audio>` query-string tokens are now short-lived, significantly reducing the log-exposure risk identified in ADR-0004

**Negative:**
- Refresh token storage requires a new database table and cleanup logic
- Every refresh request hits the database (acceptable for infrequent operation — once per 15 minutes at most)
- Frontend requires an interceptor for transparent refresh — added client-side complexity
- Token rotation means a refresh token can only be used once — if the response is lost (network failure), the user must re-login
- CSP must be carefully tested to avoid breaking existing functionality (fonts, styles, media playback)

**Neutral:**
- localStorage storage for both tokens remains (consistent with ADR-0004) — XSS risk mitigated by CSP rather than storage mechanism change
- The API response shape for login changes (adds `refreshToken` and `expiresIn` fields)
- Existing `?token=` query parameter pattern for audio continues to work — the token is just shorter-lived now
