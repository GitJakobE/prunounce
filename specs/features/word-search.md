# Feature Requirements Document — Word Search & Lookup

**Parent PRD:** [prd.md](../prd.md)
**Feature ID:** F-SEARCH
**Requirement:** REQ-5
**Priority:** P1 (High — launch feature)

## 1. Overview

Users can type a word into a search bar and, if it exists in the dictionary for their current target language, see the target-language word, its translation, and play its pronunciation. Search works in both directions: users can search by the target-language word or by a word in their chosen reference language. This provides a quick-access complement to the category-based browsing experience. Search results include both curated and user-contributed words.

## 2. User Stories

| ID | Story | Acceptance Criteria |
|---|---|---|
| US-S1 | As a user, I want to type a word and see matching results so I can quickly find a specific word. | Typing at least 2 characters shows matching results in a dropdown or results list. |
| US-S2 | As a user, I want to search in my reference language so I can find the target-language word for something I know. | Searching "bread" (English reference) while learning Italian returns "pane" with its pronunciation. |
| US-S3 | As a user, I want to search in my target language so I can look up a word I've heard. | Searching "grazie" (Italian target) returns the word entry with translation and audio. |
| US-S4 | As a user, I want to hear the pronunciation directly from the search results. | A play button is available next to each search result. |
| US-S5 | As a user, I want to be told when a word is not in the dictionary so I don't keep trying. | A clear "No results found" message is displayed when there are no matches. |
| US-S6 | As a user, I want search to find user-contributed words as well as curated words. | Contributed words appear in search results identically to curated words. |

## 3. Functional Requirements

### 3.1 Search Bar Placement
- A search bar must be accessible from every page of the application (e.g., in the header/navigation bar).
- The search bar must have clear placeholder text indicating what can be searched (e.g., "Search for a word…").

### 3.2 Search Input
- Search must accept input in the user's current target language or reference language.
- The search must be case-insensitive.
- The search should tolerate common diacritical mark omissions (e.g., searching "perche" should match "perché", searching "hojre" should match "højre").

### 3.3 Search Scope
- Search operates within the user's current target language word set only.
- If the user is learning Italian (via an Italian host), search returns Italian words and their reference-language translations.
- If the user switches target language by changing hosts, subsequent searches operate on the new language's word set.
- Both curated and user-contributed words are included in search results.

### 3.4 Search Results
- Results must appear quickly — ideally as the user types (live/autocomplete search) after a minimum of 2 characters.
- Each result must display:
  - The target-language word
  - The translation in the user's reference language
  - A play button for pronunciation
- If multiple words match, all matches must be shown in a scrollable list.
- Results should be ranked by relevance (exact match first, then prefix matches, then partial matches).

### 3.5 No Results
- If no dictionary entry matches the search term, display a clear message: "No results found for '[term]'."
- Optionally suggest similar words if a close match exists.

### 3.6 Navigation from Results
- Clicking a search result (beyond the play button) should navigate to the word's full entry within its category context, so the user can explore related words.

## 4. Edge Cases

- If the search term matches words in multiple categories, show all matches with a category label on each.
- If the user switches reference language while search results are displayed, the translations in the results should update.
- If the user switches target language (host) while search results are displayed, the results should clear since the word set has changed.
- Empty or whitespace-only search input must not trigger a search.

## 5. Acceptance Criteria

- [ ] Search bar is visible on every page.
- [ ] Searching by target-language word returns correct results.
- [ ] Searching by reference-language word returns correct target-language translations.
- [ ] Search is case-insensitive.
- [ ] Search tolerates missing diacritical marks.
- [ ] Each result shows the target-language word, translation, and a play button.
- [ ] A "No results found" message appears for unmatched searches.
- [ ] Results appear within 500 ms of the user pausing typing.
- [ ] Clicking a result navigates to the word's category context.
- [ ] User-contributed words appear in search results alongside curated words.
- [ ] Search scope changes when the user switches target language.
