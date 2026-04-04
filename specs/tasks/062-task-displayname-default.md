# Task 062: Default displayName at Registration

**Feature:** F-AUTH (Authentication & Profile)
**Priority:** P3 (Minor)
**Dependencies:** 004 (Auth Registration), 012 (Profile Management)
**Review reference:** [2026-03-30 post-fix review](../reviews/2026-03-30-post-fix-review.md) — REM-3
**PRD reference:** PB-2

## Problem

The `displayName` field is optional at registration (`RegisterInput.displayName: str | None = None`). When a user registers without providing a display name, `display_name` is stored as `NULL` in the database. Any UI surface that renders the user's display name (profile page, future "My Contributions" page, review dashboard) displays a blank value, which is confusing and looks like a bug.

The registration form labels the field as "Display name (optional)" in all three locales, so users may reasonably skip it.

## Requirements

### 1. Backend — Default displayName on registration

- When `POST /api/auth/register` receives a request with `displayName` absent or `null`, the backend must default it to the local-part of the email address (everything before the `@`)
- The default must be applied before the `User` row is persisted
- If `displayName` is provided and non-empty, use the provided value as-is (no change to current behaviour)
- The returned `AuthResponse` must reflect the resolved display name

### 2. Frontend — No changes required

- The registration form already sends `displayName` when provided and omits it when empty
- The profile page already displays and allows editing the display name
- No frontend changes are expected unless the team decides to remove the "(optional)" suffix from the label — that is out of scope for this task

## Acceptance Criteria

- [ ] Registering without `displayName` results in `display_name` being set to the email local-part (e.g., `alice@example.com` → `alice`)
- [ ] Registering with an explicit `displayName` uses the provided value unchanged
- [ ] The `AuthResponse` from `/api/auth/register` includes the resolved `displayName`
- [ ] Existing users with `NULL` display names are **not** retroactively updated (no migration)
- [ ] All existing auth and profile tests continue to pass

## Testing Requirements

- **Unit test:** Register without `displayName` → response `displayName` equals email local-part
- **Unit test:** Register with `displayName: ""` (empty string) → treated same as absent, defaults to email local-part
- **Unit test:** Register with `displayName: "Bob"` → response `displayName` equals `"Bob"`
- **Regression:** All existing `test_auth.py` and `test_profile.py` tests pass
