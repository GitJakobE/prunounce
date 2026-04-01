# Task 033: Frontend Story Library & Reading View

**Feature:** F-STORY (Story Reading)
**Priority:** P1
**Dependencies:** 029 (Story Data Model & API), 008 (Frontend Auth), 009 (Frontend Categories & Words)

## Description

Build the frontend story library page and story reading view. The story library is a top-level navigation destination equal to the existing Categories page. It displays stories grouped by difficulty level as cards with title, description, difficulty badge, and estimated reading time. The reading view renders the full story body with clickable words that trigger the translation panel.

## Technical Requirements

### Top-Level Navigation

- Add "Stories" as a top-level navigation item alongside "Categories" in the main nav bar
- Route: `/stories` for the library, `/stories/:storyId` for the reading view
- Navigation item must be visible on all screen sizes (responsive)
- Translated via i18next (`stories.nav`, `stories.title`, etc.)

### Story Library Page (`/stories`)

- Fetch stories from `GET /api/stories` on page load
- Group stories by difficulty (Beginner, Intermediate, Advanced) in collapsible sections
- Each story is rendered as a card showing:
  - Title (in the target language)
  - Description (in the user's reference language)
  - Difficulty badge with colour coding (green/amber/red)
  - Estimated reading time (from API response)
- Cards are ordered by the `order` field within each difficulty group
- Empty state: show a message when no stories are available for the user's language

### Story Reading View (`/stories/:storyId`)

- Fetch story from `GET /api/stories/:storyId`
- Display story title at the top
- Render the story body as flowing text where each word is an individually clickable element
- Word tokenisation: split body text by whitespace, preserving punctuation visually but making the core word the click target
- Clicking a word:
  1. Highlights the clicked word visually (underline or background colour)
  2. Calls `GET /api/dictionary/lookup?word=X&lang=Y` with the normalised word
  3. Displays the translation result in a bottom panel (see Translation Panel below)
- Include a "Back to Library" navigation link
- Show difficulty badge and estimated reading time in the header

### Translation Panel

- Fixed-position panel at the bottom of the reading view
- Shows the selected word and its translation when found
- Shows "Translation not available" when the word is not in the dictionary
- When a translation is found, show a small speaker icon to play the word's pronunciation via the existing audio endpoint
- Panel slides up when a word is selected, slides down or closes on tap-away or close button

### Responsive Layout

- Story library: single column on mobile, 2-column grid on tablet, 3-column on desktop
- Reading view: full-width text with comfortable line length (max-width ~65ch)
- Translation panel: full-width overlay on mobile, bottom bar on desktop
- Font sizes and line-height must support comfortable reading

### i18n

- All UI strings (navigation, headings, empty states, buttons, labels) must use i18next keys
- Add story-related keys to all three locale files (en, da, it)

## Acceptance Criteria

- [ ] "Stories" appears in the main navigation alongside "Categories"
- [ ] Story library page fetches and displays stories grouped by difficulty
- [ ] Story cards show title, description, difficulty badge, and reading time
- [ ] Clicking a story card navigates to the reading view
- [ ] Reading view renders story body with individually clickable words
- [ ] Clicking a word opens the translation panel with the result
- [ ] Translation panel shows "not available" for unknown words
- [ ] Speaker icon plays word pronunciation from existing audio API
- [ ] Back navigation returns to the story library
- [ ] Layout is responsive across mobile, tablet, and desktop
- [ ] All UI strings are translated via i18next

## Testing Requirements

- Story library renders stories grouped by difficulty
- Story cards display all required fields (title, description, badge, reading time)
- Empty state renders when no stories are returned
- Word click triggers dictionary lookup API call
- Translation panel shows correct translation for known words
- Translation panel shows "not available" for unknown words
- Speaker icon triggers audio playback
- Navigation between library and reading view works correctly
- Responsive breakpoints render correct column layouts
- i18n keys resolve for all three locales
