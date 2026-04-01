# Task 009: Frontend Categories & Word Browsing

**Feature:** F-DICT (Word Dictionary), F-HOST (Host Personas)
**Priority:** P0
**Dependencies:** 002 (Frontend Scaffolding), 005 (Backend Dictionary API), 007 (Backend Profile & Hosts API)
**ADRs:** ADR-0001 (Frontend Framework), ADR-0006 (Internationalisation)

## Description

Implement the main categories page and the category detail page for browsing words. The categories page displays the host persona banner, host selector, and category grid with progress indicators. The category detail page lists words in a scannable card layout with audio playback, difficulty filtering, and example sentences.

## Technical Requirements

### Categories Page (`/`)

- Fetch and display all categories from `GET /api/dictionary/categories`
- Each category card shows: localised name, total word count, listened count, progress bar or fraction
- Progress broken down by difficulty level
- Link to category detail page on click
- **Host Banner**: display the user's selected host persona (emoji, name, localised greeting) above the category listing
- **Host Selector**: display all four host cards in a grid; tapping a card saves the selection via `PATCH /api/profile` and updates the banner immediately

### Category Detail Page (`/categories/:id`)

- Fetch words from `GET /api/dictionary/categories/:id/words`
- Display words using the WordCard component
- Difficulty filter (tabs or buttons for beginner/intermediate/advanced/all)
- Show progress count for the current filter
- Link back to categories page

### WordCard Component

- Display: Italian word (prominent), phonetic hint (italic), reference-language translation, difficulty badge
- Listened state: visual indicator (checkmark) for words the user has listened to
- Example sentence: show Italian example in italics, reference-language translation below
- Example section hidden when no example exists for the word
- Audio play button (uses AudioButton component)

### HostBanner Component

- Shows selected host's emoji, name, and localised greeting
- Rendered above the category listing on the main page

### HostSelector Component

- Grid of host cards fetched from `GET /api/hosts`
- Each card: emoji, name, description in user's language
- Selected host highlighted with colour-coded ring
- Selection calls `PATCH /api/profile` with `{ hostId }` and updates local state

## Acceptance Criteria

- [ ] Categories page loads and displays all categories with names in the user's language
- [ ] Each category shows word count and listened progress
- [ ] Clicking a category navigates to the detail page
- [ ] Category detail page displays words with Italian word, phonetic hint, and translation
- [ ] Difficulty filter shows only words at the selected level
- [ ] WordCard displays example sentence when available
- [ ] WordCard shows listened checkmark for played words
- [ ] HostBanner displays the selected host's greeting
- [ ] HostSelector displays four host cards
- [ ] Selecting a host updates the banner and saves to the profile
- [ ] Host selection persists across page reloads

## Testing Requirements

- CategoriesPage renders categories after loading
- CategoriesPage shows category names and progress
- WordCard renders Italian word, translation, and phonetic hint
- WordCard shows listened checkmark when listened is true
- WordCard hides example section when no example exists
- WordCard shows example section when example exists
- HostBanner renders the selected host's greeting
- HostSelector renders four host cards
