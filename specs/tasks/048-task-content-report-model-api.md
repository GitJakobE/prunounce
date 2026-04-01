# Task 048: ContentReport Data Model & API

**Feature:** F-CONTENT-QA (Content Quality Assurance)
**Priority:** P1
**Dependencies:** 029 (Story Data Model & API), 004 (Backend Auth)

## Description

Add a `ContentReport` table to the database and build API endpoints for submitting error reports against stories or words. Learners can report grammar errors, wrong translations, pronunciation issues, or formatting problems without leaving the learning flow. Each report captures the content type, item identifier, error category, and an optional description.

## Technical Requirements

### Data Model

- Add a `ContentReport` table with the following columns:
  - `id` — primary key (UUID string)
  - `user_id` — foreign key to `User.id` (the reporter; `ON DELETE SET NULL`)
  - `content_type` — `"story"` or `"word"` (string, not null)
  - `content_id` — the story ID or word ID being reported (string, not null)
  - `category` — error category (string, not null). Allowed values:
    - `"grammar_spelling"` — grammar or spelling error
    - `"wrong_translation"` — incorrect translation
    - `"pronunciation"` — pronunciation/TTS issue
    - `"formatting"` — formatting or display issue
    - `"other"` — other issue
  - `description` — free-text description (string, nullable, max 500 characters)
  - `status` — report status (string, not null, default `"new"`). Values: `"new"`, `"reviewed"`, `"resolved"`, `"dismissed"`
  - `resolution_note` — reviewer's note when resolving (string, nullable)
  - `created_at` — timestamp (datetime, server default now)
  - `updated_at` — timestamp (datetime, server default now, onupdate now)
- Unique constraint on `(user_id, content_type, content_id)` where `status` is `"new"` — prevents duplicate active reports from the same user for the same item. Use application-level enforcement (not a DB constraint) since the uniqueness condition depends on status.

### API Endpoints

#### `POST /api/reports` — Submit a content report

- Request body:
  ```json
  {
    "content_type": "story",
    "content_id": "uuid-of-story",
    "category": "grammar_spelling",
    "description": "The word 'buongiornno' is misspelled"
  }
  ```
- Validates:
  - `content_type` is `"story"` or `"word"`
  - `content_id` references an existing Story or Word record
  - `category` is one of the allowed values
  - `description` is at most 500 characters (or null/empty)
  - User does not already have an active (new) report for this content item
- Response: `201 Created` with the created report
- Requires authentication (401 for unauthenticated)
- Rate limit: maximum 10 reports per user per hour (to prevent abuse)

#### `GET /api/reports` — List reports (reviewer access)

- Returns all reports, ordered by creation date descending
- Supports query parameters:
  - `status` — filter by status (`new`, `reviewed`, `resolved`, `dismissed`)
  - `content_type` — filter by `"story"` or `"word"`
  - `category` — filter by error category
  - `language` — filter by the language of the reported content
- Includes a `report_count` field: for each content item, how many total reports exist (all users, all statuses except dismissed)
- Requires authentication (401 for unauthenticated)
- Pagination: `limit` (default 50, max 100) and `offset` parameters

#### `PATCH /api/reports/{report_id}` — Update report status

- Request body:
  ```json
  {
    "status": "resolved",
    "resolution_note": "Fixed the spelling in the story seed data"
  }
  ```
- Validates:
  - `status` is one of the allowed values
  - `resolution_note` is at most 500 characters (or null)
- Response: `200 OK` with the updated report
- Requires authentication

### Response Schemas

- `ContentReportResponse`: id, user_id, content_type, content_id, category, description, status, resolution_note, created_at, updated_at
- `ContentReportListResponse`: items (list of reports), total count, report_count per content item
- `ContentReportCreateRequest`: content_type, content_id, category, description (optional)
- `ContentReportUpdateRequest`: status, resolution_note (optional)

## Acceptance Criteria

- [ ] `ContentReport` table created with all specified columns
- [ ] `POST /api/reports` creates a new report with status `"new"`
- [ ] Validation rejects invalid content_type, category, or non-existent content_id
- [ ] Duplicate active reports from same user for same item are rejected (409 Conflict)
- [ ] Description is limited to 500 characters
- [ ] `GET /api/reports` returns reports with filtering and pagination
- [ ] `GET /api/reports` includes report count per content item
- [ ] `PATCH /api/reports/{id}` updates status and resolution note
- [ ] All endpoints require authentication (401 for unauthenticated)
- [ ] Rate limiting prevents more than 10 reports per user per hour

## Testing Requirements

- Create a report for a story → returns 201 with correct fields
- Create a report for a word → returns 201 with correct fields
- Attempt duplicate report for same item by same user → returns 409
- Submit report with invalid content_type → returns 422
- Submit report with non-existent content_id → returns 404
- Submit report with description > 500 chars → returns 422
- Unauthenticated request → returns 401
- List reports with no filter → returns all reports
- List reports filtered by status → returns only matching reports
- List reports filtered by content_type → returns only matching type
- Update report status → status changes correctly
- Update with resolution note → note is persisted
- Report count is accurate (multiple users reporting same item)
