# Task 035: Story Feature Integration Testing

**Feature:** F-STORY (Story Reading)
**Priority:** P1
**Dependencies:** 029, 030, 031, 032, 033, 034 (all story tasks)

## Description

Write end-to-end integration tests for the story reading feature across both backend and frontend. These tests verify the complete user flow: browsing the story library, reading a story, tapping words for translation, and listening to narration with karaoke highlighting. Backend integration tests verify API endpoint chains; frontend integration tests verify component interactions and API integration.

## Technical Requirements

### Backend Integration Tests (Pytest + HTTPX)

Test the following flows against a seeded test database:

1. **Story browsing flow:**
   - Authenticate → GET /api/stories → verify stories grouped by difficulty → GET /api/stories/:id → verify full body returned

2. **Word lookup flow:**
   - Authenticate → GET /api/dictionary/lookup?word=ciao&lang=it → verify translation returned
   - Repeat with punctuated word (`"ciao!"`) → verify same result after normalisation
   - Repeat with unknown word → verify `{ found: false }`

3. **Narration flow:**
   - Authenticate → GET /api/stories/:id/narrate?hostId=X&speed=1.0 → verify audio/mpeg response
   - GET /api/stories/:id/timing?hostId=X&speed=1.0 → verify JSON array with word/offset/duration

4. **Access control:**
   - All story endpoints return 401 without auth token
   - Story from a different language returns 404

5. **Edge cases:**
   - Non-existent story ID returns 404
   - Invalid speed parameter returns 400
   - Invalid hostId returns 400

### Frontend Integration Tests (Vitest + React Testing Library)

Test the following component interactions with mocked API responses:

1. **Story library:**
   - Renders stories grouped by difficulty
   - Empty state renders when API returns no stories
   - Story card click navigates to reading view

2. **Reading view:**
   - Renders story body with clickable words
   - Word click opens translation panel with correct result
   - Unknown word shows "Translation not available"
   - Back button navigates to library

3. **Narration player:**
   - Play triggers API call with correct parameters
   - Speed change triggers new API call
   - Stop resets player state
   - Word highlighting activates with mock timing data

### Test Data

- Use the seeded story data from task 030
- Backend tests: create test fixtures that seed a minimal set of stories
- Frontend tests: use MSW or similar to mock API responses with realistic story data

## Acceptance Criteria

- [ ] Backend story browsing flow passes end-to-end
- [ ] Backend word lookup flow passes with exact match, punctuated, and unknown words
- [ ] Backend narration flow returns streaming audio and timing data
- [ ] All endpoints reject unauthenticated requests (401)
- [ ] Cross-language story access returns 404
- [ ] Frontend story library renders correctly with mocked data
- [ ] Frontend word click triggers lookup and displays translation
- [ ] Frontend narration player integration tests pass
- [ ] All tests pass in CI without external network dependencies

## Testing Requirements

- Backend tests use an isolated test database (SQLite in-memory or temp file)
- Frontend tests mock all API calls (no real backend dependency)
- Tests are deterministic and do not depend on execution order
- Coverage target: all story API endpoints, all frontend story components
