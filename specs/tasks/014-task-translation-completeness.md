# Task 014: UI Translation Completeness

**Feature:** F-LANG (Multi-Language Reference Support)
**Priority:** P1
**Dependencies:** 002 (Frontend Scaffolding), 008 (Frontend Auth), 009 (Frontend Categories), 011 (Frontend Search), 012 (Frontend Profile)
**ADRs:** ADR-0006 (Internationalisation)

## Description

Ensure all frontend UI strings are fully translated in both English and Danish. Review all pages and components for hardcoded strings, add missing translation keys, and verify that switching between languages produces no untranslated text.

## Technical Requirements

### Translation File Review

- Audit all React components and pages for text content
- Ensure every user-visible string uses `t('key')` from the `useTranslation()` hook
- No hardcoded English or Danish text in component JSX
- Translation keys must exist in both `en.json` and `da.json`

### Translation Coverage Areas

- **Auth pages**: login, register, form labels, error messages, links
- **Categories page**: page title, host greeting, host descriptions, category names (from API), progress labels
- **Category detail page**: difficulty filter labels, word count labels, back navigation
- **Search page**: search placeholder, no results message, loading indicator
- **Profile page**: field labels, buttons, confirmation dialog, success/error messages
- **Layout**: header title, navigation links, logout button
- **Common**: loading states, generic error messages

### Validation

- Manually switch language and verify every page shows fully translated text
- Verify that language switching preserves navigation context (stays on same page)
- Verify that the selected language persists across page reloads for authenticated users

## Acceptance Criteria

- [ ] All UI strings in `en.json` have corresponding entries in `da.json`
- [ ] No hardcoded text in any component or page
- [ ] Switching to Danish translates every visible string
- [ ] Switching back to English restores all text
- [ ] Language switch does not cause navigation or page reload
- [ ] Error messages from the API are displayed in the user's language where possible
- [ ] Placeholder text in inputs is translated

## Testing Requirements

- Both translation files parse without errors
- Both translation files have identical key structures
- Language switcher toggles i18next language
- Components render translated text for both languages
