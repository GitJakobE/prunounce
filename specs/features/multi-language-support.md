# Feature Requirements Document — Multi-Language Learning

**Parent PRD:** [prd.md](../prd.md)
**Feature ID:** F-LANG
**Priority:** P0 (Must-have for launch)

## 1. Overview

The platform supports learning pronunciation in multiple target languages. At launch, users can learn Italian, Danish, or English. Each user has two independent language settings:

- **Target language** — the language the user wants to learn to pronounce. This is implicitly set by choosing a host persona (Italian hosts → Italian target language, etc.).
- **Reference language** — the language the user understands, used for translations and UI text. Users can choose any supported language except their current target language as their reference language.

The system must be designed so that adding a new target or reference language requires only new content (host personas, seed data, TTS voice assignments, translations) and a database migration — not changes to application logic.

## 2. User Stories

| ID | Story | Acceptance Criteria |
|---|---|---|
| US-L1 | As a first-time user, I want to select a host persona which sets my target language, so I immediately know what language I'll be learning. | Choosing a host sets the target language; word lists and audio reflect that language. |
| US-L2 | As a user, I want to choose my reference language independently, so I see translations in the language I understand best. | A language switcher lets users pick any supported language except their current target language as the reference language. |
| US-L3 | As a returning user, I want both my target and reference language preferences remembered, so I don't have to set them every time. | Both preferences persist in the user's profile and are applied automatically on login. |
| US-L4 | As a user, I want to switch my reference language at any time from any page, so I can compare translations or change my mind. | A language switcher is accessible from every page; switching updates all visible text without a full page reload. |
| US-L5 | As a Danish speaker, I want to learn English or Italian pronunciation with Danish translations. | Choosing a Danish reference language shows all UI and translations in Danish. |
| US-L6 | As an English speaker, I want to learn Danish or Italian pronunciation with English translations. | Choosing an English reference language shows all UI and translations in English. |
| US-L7 | As an Italian speaker, I want to learn Danish or English pronunciation with Italian translations. | Choosing an Italian reference language shows all UI and translations in Italian. |

## 3. Functional Requirements

### 3.1 Target Language
- The target language is determined by the user's chosen host persona (see host-personas FRD).
- Each host belongs to exactly one language. Selecting a host implicitly sets the target language.
- The target language determines which words are displayed and which TTS voice is used for pronunciation audio.
- Changing hosts to a different language changes the target language accordingly.

### 3.2 Reference Language
- A reference language picker must be available on every page (e.g., in the header, top-right area).
- At launch, the picker offers Italian, Danish, and English — minus the user's current target language.
- The selected reference language is stored as part of the user's profile.
- Switching the reference language updates all visible UI text, word translations, and descriptions without requiring a full page reload.

### 3.3 Localisation of UI
- All navigation labels, buttons, headings, instructions, error messages, and informational text must be available in Italian, Danish, and English.
- Switching the reference language must update all visible text without losing navigation context.

### 3.4 Localisation of Content
- Every word entry in the dictionary must have translations in all supported reference languages.
- Word descriptions, phonetic hints, and category names must also be localised.

### 3.5 Supported Language Combinations at Launch

| Target Language (learning) | Available Reference Languages |
|---|---|
| Italian | Danish, English |
| Danish | Italian, English |
| English | Italian, Danish |

### 3.6 Extensibility
- Adding a new language requires: new host personas, new TTS voice assignments, seed data with word entries, translations for all existing reference languages, and a database migration to add translation columns. No application logic changes should be required.

## 4. Edge Cases

- If a translation for a specific word is missing in the user's reference language, display the English translation as a fallback with a visual indicator that the translation is approximate.
- If the user has not yet selected a host and is not logged in, default to English as the reference language.
- When a user switches host to a different language, their word progress for the previous target language is preserved and available if they switch back.

## 5. Acceptance Criteria

- [ ] Users can learn pronunciation in Italian, Danish, or English by choosing an appropriate host.
- [ ] Reference language can be set independently of target language.
- [ ] UI is fully translated in Italian, Danish, and English with no untranslated strings.
- [ ] Every word has translations in all three supported languages.
- [ ] Both target and reference language preferences persist across sessions.
- [ ] Switching reference language updates all text in place without losing navigation state.
- [ ] English is used as fallback when a translation is missing.
- [ ] Progress is preserved per target language when switching hosts.
