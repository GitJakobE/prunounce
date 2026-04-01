# Task 004: Backend Authentication API

**Feature:** F-AUTH (User Authentication)
**Priority:** P0
**Dependencies:** 001 (Backend Scaffolding)
**ADRs:** ADR-0004 (JWT Authentication)

## Description

Implement the authentication API endpoints: user registration, login, Google social login, session validation, and password hashing. All endpoints issue stateless JWTs. The auth middleware must accept tokens from both the Authorization header and a query parameter fallback (for audio element compatibility).

## Technical Requirements

### Endpoints

- `POST /api/auth/register` — Create account with email, password, language, optional displayName. Validate email format, password strength (min 8 chars, uppercase, lowercase, digit). Hash password with bcryptjs. Return JWT + user object.
- `POST /api/auth/login` — Authenticate with email and password. Return JWT + user object. Non-specific error messages for failed attempts.
- `POST /api/auth/google` — Validate Google OAuth credential server-side. Create or link account. Return JWT + user object.
- `GET /api/auth/me` — Return current user from token. Protected by auth middleware.

### Auth Middleware

- Check `Authorization: Bearer <token>` header first
- Fall back to `req.query.token` if no header present
- Verify JWT signature and expiry using jsonwebtoken
- Attach `userId` to the request object
- Return 401 for missing or invalid tokens

### Security

- Passwords hashed with bcryptjs (automatic salt)
- JWT signed with configurable secret, 30-day expiry
- express-validator for input validation on registration
- Non-specific error messages on login failure

## Acceptance Criteria

- [ ] Users can register with email and password
- [ ] Duplicate email registration returns a clear error
- [ ] Password must meet complexity requirements (rejected if too weak)
- [ ] Users can log in with valid credentials and receive a JWT
- [ ] Invalid credentials return 401 with a non-specific error message
- [ ] `GET /api/auth/me` returns the current user for a valid token
- [ ] `GET /api/auth/me` returns 401 for an invalid or expired token
- [ ] Auth middleware accepts tokens from both header and query parameter
- [ ] Passwords are never stored in plain text

## Testing Requirements

- Registration creates a user and returns a valid JWT
- Registration rejects duplicate emails with 409 or appropriate status
- Registration rejects weak passwords with validation errors
- Login succeeds with correct credentials
- Login fails with wrong password (401)
- Login fails with non-existent email (401, same error message)
- Auth middleware accepts Bearer token in header
- Auth middleware accepts token in query parameter
- Auth middleware rejects missing token (401)
- Auth middleware rejects invalid token (401)
