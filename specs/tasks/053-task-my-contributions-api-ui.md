# Task 053: My Contributions API & Frontend

**Feature:** F-UGC (User-Contributed Words)
**Priority:** P2
**Dependencies:** 022 (User-Contributed Words API), 026 (Frontend Word Contribution)
**Review reference:** [2026-03-30 post-fix review](../reviews/2026-03-30-post-fix-review.md) — REM-5
**ADRs:** ADR-0018 (User Content Trust Model)

## Problem

Users can contribute words to the shared dictionary via `POST /api/dictionary/words`, but there is no way for a user to view, manage, or track their own contributions. The review panel noted this as a gap for both Aiden (who wants to verify his contributions were accepted) and Nikolaj (a power contributor who wants to see what he has added).

## Requirements

### 1. Backend — My Contributions endpoint

- `GET /api/dictionary/words/me` — returns all words contributed by the authenticated user
- Protected by auth middleware (401 for unauthenticated requests)
- Response: array of word objects, each including:
  - `wordId`, `word`, `language`
  - `translationEn`, `translationDa`, `translationIt`
  - `phoneticHint`, `difficulty`
  - `categoryId`, `categoryName` (resolved in user's reference language)
  - `createdAt` timestamp
- Default sort: newest first (`createdAt DESC`)
- Optional query parameter: `?lang=<language>` to filter by target language
- Empty array if the user has not contributed any words

### 2. Frontend — My Contributions page

- Add a `/my-contributions` route accessible from the user profile page or the navigation
- Display the user's contributed words in a card or list layout
- Each entry shows: word, translation(s), category name, difficulty badge, date added
- If the user has no contributions, show an encouraging empty-state message (use i18n key)
- Include a link/button to the Add Word page for convenience
- Page must be responsive (mobile, tablet, desktop) and accessible (labels, keyboard navigation)

### 3. i18n

- Add new i18n keys to `en.json`, `da.json`, and `it.json`:
  - `contributions.title` — page heading (e.g., "My Contributions")
  - `contributions.empty` — empty state message (e.g., "You haven't contributed any words yet. Add your first word!")
  - `contributions.addWord` — link text to Add Word page
  - `contributions.dateAdded` — label for date column/badge

## Acceptance Criteria

- [ ] `GET /api/dictionary/words/me` returns all words with `contributedBy = current user`
- [ ] Response includes resolved category names in the user's reference language
- [ ] Results are sorted by `createdAt DESC` (newest first)
- [ ] Optional `?lang=` filter scopes results to a single target language
- [ ] Empty contributions return `[]` with 200 status
- [ ] Unauthenticated requests return 401
- [ ] Frontend `/my-contributions` page renders the user's contributions
- [ ] Empty state shows localised encouragement message with link to Add Word
- [ ] Page is responsive across mobile, tablet, and desktop breakpoints
- [ ] Page is accessible: proper headings, labels, keyboard navigation
- [ ] i18n keys added to all three locale files

## Testing Requirements

- **Backend unit tests:**
  - User with 0 contributions → 200, empty array
  - User with 3 contributions → 200, array of 3 words sorted by createdAt DESC
  - `?lang=da` filter returns only Danish words
  - Unauthenticated request → 401
  - Contributed words from other users are excluded
- **Frontend unit tests:**
  - Renders contributions list when API returns words
  - Renders empty state when API returns empty array
  - Link to Add Word page is present in empty state
- **Regression:** All existing backend and frontend tests pass
- **Manual:** Navigate to My Contributions, verify contributed words appear, verify empty state for new user
