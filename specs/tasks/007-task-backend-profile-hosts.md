# Task 007: Backend Profile & Host Personas API

**Feature:** F-AUTH (Profile/GDPR), F-HOST (Host Personas)
**Priority:** P0
**Dependencies:** 001 (Backend Scaffolding), 004 (Backend Auth)
**ADRs:** ADR-0004 (Authentication)

## Description

Implement the user profile management endpoints (view, update, delete) and the host personas listing endpoint. Profile updates include language preference and host persona selection. Account deletion must cascade-remove all user data (GDPR compliance).

## Technical Requirements

### Profile Endpoints

- `GET /api/profile` — Return the authenticated user's profile (id, email, displayName, language, hostId) and progress summary (totalWords, listenedWords). Protected by auth middleware.
- `PATCH /api/profile` — Update profile fields: displayName, referenceLanguage (validated against `["en", "da", "it"]`), hostId (validated against known host IDs). Return the updated user. At least one field must be provided.
- `DELETE /api/profile` — Delete the user's account and all associated data. Prisma cascade deletes handle UserProgress records. Return 204 No Content.

### Host Personas Endpoint

- `GET /api/hosts` — Return the list of all available host personas. Each host includes: id, name, emoji, descriptions (per language), greetings (per language), colour accent. This endpoint does NOT require authentication (hosts are public data).

### Host Data

- Host definitions stored as a static data module (not in the database)
- Twelve hosts at launch — four per target language:
  - **Italian:** Marco (chef), Giulia (professor), Luca (student), Sofia (grandmother)
  - **Danish:** Anders (barista), Freja (journalist), Mikkel (design student), Ingrid (grandmother)
  - **English:** James (professor), Emma (professor), Ryan (host), Margaret (grandmother)
- Each host has: id, name, language, descriptions in all three languages (EN / DA / IT), greetings in all three languages, colour accent, TTS voice assignment

## Acceptance Criteria

- [ ] `GET /api/profile` returns the user's profile with progress stats
- [ ] `PATCH /api/profile` updates displayName successfully
- [ ] `PATCH /api/profile` updates language with validation (only `"en"`, `"da"`, or `"it"` accepted)
- [ ] `PATCH /api/profile` updates hostId with validation (only valid host IDs accepted)
- [ ] `PATCH /api/profile` rejects requests with no update fields
- [ ] `DELETE /api/profile` removes the user and all associated data
- [ ] `DELETE /api/profile` returns 204
- [ ] `GET /api/hosts` returns all twelve host personas (4 × IT, 4 × DA, 4 × EN)
- [ ] `GET /api/hosts` does not require authentication
- [ ] Profile endpoints return 401 for unauthenticated requests

## Testing Requirements

- Profile GET returns correct user data and progress
- Profile PATCH updates displayName
- Profile PATCH updates language preference
- Profile PATCH rejects invalid language values
- Profile PATCH updates hostId
- Profile PATCH rejects invalid hostId values
- Profile PATCH rejects empty update body
- Profile DELETE removes user and returns 204
- Profile DELETE cascades to UserProgress records
- Hosts GET returns all hosts without authentication
- Profile endpoints reject unauthenticated requests
