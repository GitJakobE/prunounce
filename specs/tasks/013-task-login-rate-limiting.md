# Task 013: Login Rate Limiting

**Feature:** F-AUTH (Security — Login Rate Limiting)
**Priority:** P1
**Dependencies:** 004 (Backend Auth API)
**ADRs:** ADR-0004 (Authentication)

## Description

Add rate limiting to the login endpoint to mitigate brute-force attacks. After a configurable number of failed login attempts for the same email within a time window, subsequent attempts must be temporarily blocked.

## Technical Requirements

### Rate Limiting Logic

- Track failed login attempts per email address
- Configurable threshold: default 5 failed attempts within a 15-minute window
- When threshold is exceeded, block login attempts for that email with HTTP 429 and a clear error message: "Too many login attempts. Please try again in 15 minutes."
- Rate limit counter resets after the time window expires
- Successful login resets the counter for that email
- Rate limiting must not reveal whether the email exists (blocked message is the same regardless)

### Implementation Considerations

- In-memory rate limit store is acceptable for a single-server deployment
- Store structure: Map of email → { attempts: number, firstAttemptAt: Date }
- Clean up expired entries periodically to prevent memory leaks
- Consider using an existing rate-limiting middleware library (e.g., `express-rate-limit`) or a custom implementation

### Scope

- Rate limiting applies only to the `POST /api/auth/login` endpoint
- Registration endpoint does NOT need rate limiting (account creation has natural friction)
- The `GET /api/auth/me` endpoint does not need rate limiting

## Acceptance Criteria

- [ ] Login endpoint allows up to 5 failed attempts within 15 minutes
- [ ] The 6th failed attempt within the window returns HTTP 429
- [ ] The error message does not reveal whether the email exists
- [ ] After the time window expires, login attempts are allowed again
- [ ] A successful login resets the failure counter
- [ ] Rate limiting does not affect valid logins when under the threshold
- [ ] Memory usage remains bounded (expired entries are cleaned up)

## Testing Requirements

- Login succeeds when under the rate limit threshold
- Login returns 429 after exceeding the failed attempt threshold
- Error message is non-specific (does not reveal email existence)
- Rate limit resets after the time window expires
- Successful login resets the failure counter
- Rate limiting does not affect other email addresses
