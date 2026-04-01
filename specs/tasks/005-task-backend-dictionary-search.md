# Task 005: Backend Dictionary & Search API

**Feature:** F-DICT (Word Dictionary), F-SEARCH (Word Search)
**Priority:** P0
**Dependencies:** 001 (Backend Scaffolding), 003 (Content Seeding)
**ADRs:** ADR-0003 (Database), ADR-0006 (Internationalisation)

## Description

Implement the dictionary browsing and word search API endpoints. Dictionary endpoints return categories and words with translations in the user's reference language. Search supports querying by Italian word or reference-language translation. All endpoints are protected by the auth middleware.

## Technical Requirements

### Dictionary Endpoints

- `GET /api/dictionary/categories` — Return all categories with word counts and progress per category. Accepts `?lang=en|da` to determine which translation columns to return. Category names returned as a generic `name` field (mapped from `nameEn`/`nameDa`). Include `totalWords`, `listenedWords`, and `progressByDifficulty` per category.
- `GET /api/dictionary/categories/:id/words` — Return all words in a category. Accepts `?lang=en|da` and optional `?difficulty=beginner|intermediate|advanced`. Each word includes: `id`, `italian`, `phoneticHint`, `translation` (mapped from language column), `difficulty`, `listened` (boolean from UserProgress), `example` (translated example), `exampleIt` (Italian example).

### Search Endpoint

- `GET /api/search?q=<term>&lang=en|da` — Search words by Italian word or reference-language translation. Case-insensitive matching using Prisma `contains` with `mode: "insensitive"`. Return matching words with the same shape as the dictionary word endpoint. Return empty array with no error if no matches found.

### Shared Behaviour

- All endpoints require authentication (auth middleware)
- Language selection via `?lang` parameter (default: "en")
- Translation column mapping: `lang=en` → `translationEn`, `lang=da` → `translationDa`
- Progress data includes UserProgress records for the authenticated user

## Acceptance Criteria

- [ ] `GET /api/dictionary/categories` returns all seeded categories with correct word counts
- [ ] Categories include per-user progress (listened word count)
- [ ] `GET /api/dictionary/categories/:id/words` returns words for the given category
- [ ] Words include translated fields based on the `lang` parameter
- [ ] Words include the user's listened status
- [ ] Difficulty filtering works correctly when `?difficulty` is provided
- [ ] `GET /api/search?q=ciao` returns matching Italian words
- [ ] `GET /api/search?q=hello&lang=en` returns words whose English translation matches
- [ ] Search is case-insensitive
- [ ] Search with no matches returns an empty array (not an error)
- [ ] All endpoints return 401 for unauthenticated requests

## Testing Requirements

- Categories endpoint returns all categories with correct structure
- Categories include progress data for the authenticated user
- Words endpoint returns words for a valid category ID
- Words endpoint filters by difficulty when parameter is provided
- Words endpoint returns 404 for a non-existent category
- Search returns results for Italian word queries
- Search returns results for English translation queries
- Search returns results for Danish translation queries
- Search is case-insensitive
- Search returns empty array for unmatched queries
- All endpoints reject unauthenticated requests with 401
