# Task 038: Story Translation Panel Must Use User's Reference Language

**Feature:** F-STORY (Story Reading), F-LANG (Multi-Language Support)
**Priority:** P0 (Bug fix — core feature not working as specified)
**Dependencies:** 032 (Story Word Lookup API), 033 (Frontend Story Library & Reading)

## Problem

When a user clicks a word in Story Reading mode, the translation panel always displays the English translation regardless of the user's chosen reference language. For example, a Danish-speaking user learning Italian with their reference language set to Danish sees English translations instead of Danish.

This violates multiple existing requirements:

- **Story Reading FRD §3.5:** "The translation in the user's reference language"
- **Story Reading FRD US-S6:** "Clicking a word in the story text populates the translation panel with that word's translation in the user's reference language."
- **Story Reading FRD §3.9:** "The translation panel translates clicked words into the user's reference language."
- **Multi-Language FRD §3.2:** "The selected reference language is stored as part of the user's profile."
- **PRD REQ-14:** "…showing the reference-language translation, phonetic hint, and a play button…"

## Root Cause

The word lookup flow does not respect the user's stored reference language preference:

1. The frontend calls the lookup endpoint **without** passing the user's reference language.
2. The backend's fallback logic defaults to English (or Danish when the target language is English) instead of reading the user's profile to determine their actual reference language.

## Expected Behaviour

- When a user clicks any word in a story, the translation shown in the translation panel **must** be in the user's currently selected reference language.
- If the user has set Danish as their reference language, they see Danish translations.
- If the user has set Italian as their reference language, they see Italian translations.
- If the user has set English as their reference language, they see English translations.
- The behaviour must be consistent with how translations work in the Categories section and the word dictionary elsewhere in the app.

## Acceptance Criteria

- [ ] Clicking a word in a story shows the translation in the user's selected reference language, not a hardcoded default.
- [ ] A user with reference language set to Danish sees Danish translations in the story translation panel.
- [ ] A user with reference language set to Italian sees Italian translations in the story translation panel.
- [ ] A user with reference language set to English sees English translations in the story translation panel.
- [ ] Switching the reference language via the language switcher immediately affects subsequent word lookups in story mode.
- [ ] The fix does not break word translations in Categories mode or the search feature.
- [ ] The fallback behaviour (when a specific translation is missing) still falls back to English, as specified in the Multi-Language FRD §4.

## Scope

This task fixes the story word lookup translation language only. It does not change:

- Story narration or TTS behaviour
- Story descriptions or library display
- Dictionary browsing outside of story mode
