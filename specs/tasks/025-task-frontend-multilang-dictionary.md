# Task 025: Frontend Multi-Language Dictionary & Search

**Feature:** F-DICT (Word Dictionary), F-SEARCH (Word Search), F-LANG (Multi-Language)
**Priority:** P0
**Dependencies:** 019 (Multi-Language Dictionary API), 024 (Host-First Landing)

## Description

Update all frontend dictionary and search pages to work with the multi-language API. The frontend must display words in the user's target language, show translations in the reference language, and adapt when the user switches hosts or reference language.

## Technical Requirements

### TypeScript Type Updates
- Rename the `italian` field to `word` in the `WordEntry` interface
- Add `language` field if needed for display purposes

### API Service Updates
- Update all API call functions (`getCategories`, `getCategoryWords`, `searchWords`) to pass the reference language as a `?lang=` parameter
- The reference language should come from the i18n current language setting
- Remove any hardcoded assumptions about Italian as the target language

### CategoriesPage Updates
- Category names displayed using the reference language (already handled server-side via `?lang`)
- Progress counts reflect only words in the current target language

### CategoryDetailPage Updates
- Word cards display the `word` field (target language) instead of `italian`
- Translations shown in the reference language
- Example sentences shown in both target and reference languages
- Audio playback works with the target-language word

### SearchPage Updates
- Search queries operate on the target-language word set
- Search results show the `word` field and reference-language translation
- Audio playback from search results works correctly

### WordCard Component Updates
- Rename `italian` prop/display to `word`
- Ensure phonetic hint, translation, and example sentence adapt to the current language context

### Language Switch Reactivity
- When the user switches reference language (via LanguageSwitcher), re-fetch displayed data to get updated translations
- When the user switches hosts (via host switcher), re-fetch the entire word set since the target language may have changed

## Acceptance Criteria

- [ ] Dictionary pages display words in the user's target language (not hardcoded Italian)
- [ ] Translations are shown in the user's chosen reference language
- [ ] Switching reference language updates translations without full page reload
- [ ] Switching hosts reloads the word set for the new target language
- [ ] Search works within the current target language
- [ ] WordCard displays `word` instead of `italian`
- [ ] Audio playback works for all three target languages
- [ ] Progress indicators reflect per-language progress

## Testing Requirements

- WordCard renders the `word` field correctly
- API calls include the correct `lang` parameter
- Category pages re-render when reference language changes
- Search results match the correct target language
