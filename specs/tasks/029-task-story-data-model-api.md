# Task 029: Story Data Model & API

**Feature:** F-STORY (Story Reading)
**Priority:** P1
**Dependencies:** 017 (Schema Migration — Multi-Language), 019 (Multi-Language Dictionary API)

## Description

Add a `Story` table to the database and implement the API endpoints for listing and retrieving stories. Stories are curated long-form text content organised by target language and difficulty level. The API must support filtering by language and difficulty, and return all fields needed by the frontend story library and reading view.

## Technical Requirements

### Data Model

- Add a `Story` table with the following columns:
  - `id` — primary key (UUID string)
  - `slug` — URL-friendly identifier (e.g., `cafe-introduction`)
  - `language` — target language code (`it`, `da`, `en`)
  - `difficulty` — one of `beginner`, `intermediate`, `advanced`
  - `title` — story title in the target language
  - `descriptionEn` — short description in English
  - `descriptionDa` — short description in Danish
  - `descriptionIt` — short description in Italian
  - `body` — full story text in the target language (TEXT column)
  - `order` — display order within difficulty group (integer)
- Unique constraint on `(slug, language)` — same slug can exist across languages but not within one language
- Follow the existing column-per-language pattern used by `Category` and `Word` (ADR-0006)

### API Endpoints

- `GET /api/stories` — list stories for the user's target language
  - Filters by the target language derived from the user's selected host
  - Groups results by difficulty level
  - Returns: id, slug, language, difficulty, title, description (in user's reference language), estimated reading time
  - Estimated reading time is computed from body word count (average reading speed: 150 words/minute for language learners)
  - Protected by auth middleware

- `GET /api/stories/:storyId` — get a single story with full body text
  - Returns all fields including the full `body` text
  - Returns the description in the user's reference language
  - Protected by auth middleware
  - Returns 404 if story not found or belongs to a different target language

### Reference Language Resolution

- Use the same pattern as the dictionary API: determine the user's reference language from their profile, and return only the matching description field (e.g., `descriptionEn` when reference language is `en`)

## Acceptance Criteria

- [ ] `Story` table is created with all specified columns
- [ ] `(slug, language)` unique constraint is enforced
- [ ] `GET /api/stories` returns stories filtered by the user's target language
- [ ] Stories are grouped by difficulty in the response
- [ ] Each story in the list includes an estimated reading time
- [ ] `GET /api/stories/:storyId` returns the full story body
- [ ] Description is returned in the user's reference language only
- [ ] 404 is returned for non-existent or wrong-language stories
- [ ] Both endpoints require authentication (401 for unauthenticated)

## Testing Requirements

- Story listing returns only stories matching the user's host language
- Story listing groups stories by difficulty level
- Estimated reading time is computed correctly (word count / 150, rounded up)
- Story detail returns full body text
- Story detail returns description in the user's reference language
- Non-existent story ID returns 404
- Story belonging to a different language returns 404
- Unauthenticated requests return 401
