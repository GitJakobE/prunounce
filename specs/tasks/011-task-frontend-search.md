# Task 011: Frontend Word Search

**Feature:** F-SEARCH (Word Search & Lookup)
**Priority:** P1
**Dependencies:** 002 (Frontend Scaffolding), 005 (Backend Dictionary & Search API)
**ADRs:** ADR-0001 (Frontend Framework)

## Description

Implement the search page where users can type a word (in Italian or their reference language) and see matching results with translations and audio playback. The search must be responsive, case-insensitive, and provide clear feedback when no results are found.

## Technical Requirements

### Search Page (`/search`)

- Search input with placeholder text (localised: "Search for a word…")
- Debounced search: trigger API call after the user pauses typing (~300ms debounce, minimum 2 characters)
- Call `GET /api/search?q={term}&lang={userLanguage}`
- Display results as WordCard components (same as category detail page)
- Show "No results found for '{term}'" when search returns empty
- Show loading indicator while search is in progress
- Clear results when input is emptied

### Navigation

- Search page accessible from the layout header (search icon or link)
- Search accessible from every page via the header

### Search Behaviour

- Case-insensitive matching
- Tolerant of missing diacritical marks (handled server-side)
- Empty or whitespace-only input does not trigger a search

## Acceptance Criteria

- [ ] Search input is displayed on the search page
- [ ] Typing at least 2 characters triggers a debounced API call
- [ ] Results display as word cards with Italian word, translation, phonetic hint, and play button
- [ ] "No results found" message appears for unmatched queries
- [ ] Search works for both Italian words and reference-language translations
- [ ] Search is case-insensitive
- [ ] Loading indicator shows during API calls
- [ ] Empty input clears results
- [ ] Search is accessible from the header on every page

## Testing Requirements

- Search page renders the search input
- Search triggers API call after typing 2+ characters
- Results render as word cards
- "No results" message renders for empty results
- Empty input does not trigger a search
