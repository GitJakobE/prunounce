# Task 023: Italian UI Translations

**Feature:** F-LANG (Multi-Language Learning)
**Priority:** P1
**Dependencies:** None (can be done in parallel with backend tasks)

## Description

Add Italian as a third UI/reference language for the frontend. Currently the app supports English and Danish UI translations via i18next. Italian must be added as a full UI translation so that users who select Italian as their reference language see all interface text in Italian.

## Technical Requirements

### i18n Translation File
- Create `src/frontend/src/i18n/it.json` containing Italian translations for all UI strings
- The key structure must exactly match the existing `en.json` and `da.json` files
- All keys present in `en.json` must be present in `it.json`

### i18n Configuration
- Register the Italian locale in the i18n configuration
- Add Italian as an option in the language switcher component

### Language Switcher Update
- Update the `LanguageSwitcher` component to include Italian as a third option
- Display appropriate labels: "English", "Dansk", "Italiano"
- The switcher must exclude the user's current target language from the reference language options

### Reference Language Logic
- When a user selects an Italian host (target = Italian), the reference language picker should offer English and Danish only (not Italian)
- When a user selects a Danish host (target = Danish), the reference language picker should offer English and Italian
- When a user selects an English host (target = English), the reference language picker should offer Danish and Italian

## Acceptance Criteria

- [ ] `it.json` contains all keys present in `en.json` and `da.json`
- [ ] Selecting Italian in the language switcher displays all UI text in Italian
- [ ] The language switcher shows three options (minus the target language)
- [ ] No untranslated strings appear when Italian is selected
- [ ] Switching languages in-place does not lose navigation context

## Testing Requirements

- Italian translation file has the same key count as English and Danish files
- Language switcher renders the correct options based on target language
- Switching to Italian updates all visible UI text
- No missing translation warnings in the browser console when Italian is active
