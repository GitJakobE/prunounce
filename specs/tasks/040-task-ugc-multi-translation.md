# Task 040: UGC Multi-Translation Strategy

**Feature:** F-UGC (User-Contributed Words), F-LANG (Multi-Language Support)
**Priority:** P1
**Dependencies:** 022 (User-Contributed Words API), 026 (Frontend Word Contribution)
**Review reference:** [2026-03-29 review](../reviews/2026-03-29-current-state.md) — CUT-2

## Problem

When a user contributes a new word via `POST /api/dictionary/words`, the backend stores the provided `translation` into only the column matching the contributor's current reference language. The other two translation columns are stored as empty strings. This means:

- Aiden (English ref) contributes "hyggelig" → `translation_en = "cozy"`, `translation_da = ""`, `translation_it = ""`
- When Patrizia (Italian ref) browses the same word, she sees a blank translation
- When Mette (Danish ref) browses it, she also sees a blank translation

This directly undermines the multi-language value proposition and creates a degraded experience for 2 out of 3 language groups for every user-contributed word.

## Requirements

### Backend Changes

- Update `POST /api/dictionary/words` to accept **all three translation fields** explicitly:
  - `translationEn` (optional, string) — English translation
  - `translationDa` (optional, string) — Danish translation
  - `translationIt` (optional, string) — Italian translation
- **At least one** translation must be provided (the one matching the contributor's reference language is required by the existing validation; the others are optional but encouraged)
- The existing `translation` field remains accepted as a fallback for backward compatibility — if only `translation` is provided, it is stored in the contributor's reference language column as today
- If individual `translationXx` fields are provided, they take precedence over the generic `translation` field

### Frontend Changes

- Update the Add Word form to show **three translation fields** instead of one:
  - The field matching the user's reference language is **required** (pre-labelled, e.g., "English translation (required)")
  - The other two fields are **optional** (labelled with the language name, e.g., "Italian translation (optional)")
- The user's reference language translation field should appear first
- Display a helper message encouraging users to fill in all translations: "Adding translations in all languages helps other learners"

### Display of Incomplete Translations

- When a word has a blank translation in the user's reference language, display a placeholder: "No [language] translation yet" (localised)
- Optionally, display a "Add translation" link/button on the word card so other users can fill in missing translations (stretch goal — may be deferred)

## Acceptance Criteria

- [ ] `POST /api/dictionary/words` accepts `translationEn`, `translationDa`, `translationIt` fields
- [ ] If all three are provided, all columns are populated
- [ ] If only `translation` is provided, only the contributor's reference language column is filled (backward compatible)
- [ ] At least one non-empty translation is required (400 if none provided)
- [ ] The frontend Add Word form shows three translation fields with appropriate required/optional labels
- [ ] The reference language field is required and appears first
- [ ] Words with missing translations display a localised placeholder instead of blank
- [ ] All new i18n keys are added to `en.json`, `da.json`, `it.json`

## Testing Requirements

- Backend: contributing with all three translations populates all columns
- Backend: contributing with only `translation` + ref lang populates one column, others empty (backward compatibility)
- Backend: contributing with no translations returns 400
- Frontend: form renders three translation fields
- Frontend: required field is enforced for the reference language
- Frontend: blank translations display the localised placeholder in word cards
