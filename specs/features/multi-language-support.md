# Feature Requirements Document — Multi-Language Learning

**Parent PRD:** [prd.md](../prd.md)
**Feature ID:** F-LANG
**Priority:** P0 (Must-have for launch)

## 1. Overview

The platform supports learning pronunciation in multiple target languages, with the ambition to scale to many languages over time — including less widely spoken languages such as Icelandic and Swedish. The core value proposition is that a learner can study a smaller language using a more widely known language as their reference, or vice versa.

At launch, users can learn Italian, Danish, English, or Spanish. Each user has two independent language settings:

- **Target language** — the language the user wants to learn to pronounce. This is implicitly set by choosing a host persona (Italian hosts → Italian target language, etc.).
- **Reference language** — the language the user understands, used for translations and UI text. Users can choose any supported language except their current target language as their reference language.

The system must be designed so that adding a new target or reference language requires only new content (host personas, seed data, TTS voice assignments, translations, UI translation file) and configuration — not changes to application logic or database schema restructuring. The set of supported languages must be data-driven, not hard-coded in conditionals or switch statements.

## 2. User Stories

| ID | Story | Acceptance Criteria |
|---|---|---|
| US-L1 | As a first-time user, I want to select a host persona which sets my target language, so I immediately know what language I'll be learning. | Choosing a host sets the target language; word lists and audio reflect that language. |
| US-L2 | As a user, I want to choose my reference language independently, so I see translations in the language I understand best. | A language switcher lets users pick any supported language except their current target language as the reference language. |
| US-L3 | As a returning user, I want both my target and reference language preferences remembered, so I don't have to set them every time. | Both preferences persist in the user's profile and are applied automatically on login. |
| US-L4 | As a user, I want to switch my reference language at any time from any page, so I can compare translations or change my mind. | A language switcher is accessible from every page; switching updates all visible content (UI labels, category names, story descriptions, word translations) without a full page reload. |
| US-L5 | As a Danish speaker, I want to learn English, Italian, or Spanish pronunciation with Danish translations. | Choosing a Danish reference language shows all UI and translations in Danish. |
| US-L6 | As an English speaker, I want to learn Danish, Italian, or Spanish pronunciation with English translations. | Choosing an English reference language shows all UI and translations in English. |
| US-L7 | As an Italian speaker, I want to learn Danish, English, or Spanish pronunciation with Italian translations. | Choosing an Italian reference language shows all UI and translations in Italian. |
| US-L8 | As a Spanish speaker, I want to learn Danish, English, or Italian pronunciation with Spanish translations. | Choosing a Spanish reference language shows all UI and translations in Spanish. |
| US-L9 | As an administrator adding a new language, I want to be able to introduce it by providing only content and configuration files, so that no code changes are needed. | A new language can be made available by adding: host personas, seed data, TTS voice assignments, translations for existing content, and a UI translation file — without modifying application logic or restructuring the database. |

## 3. Functional Requirements

### 3.1 Target Language
- The target language is determined by the user's chosen host persona (see host-personas FRD).
- Each host belongs to exactly one language. Selecting a host implicitly sets the target language.
- The target language determines which words are displayed and which TTS voice is used for pronunciation audio.
- Changing hosts to a different language changes the target language accordingly.

### 3.2 Reference Language
- A reference language picker must be available on every page (e.g., in the header, top-right area).
- The picker must be a **compact dropdown menu** — not a row of buttons or other prominent control. Users change their reference language infrequently, so it should be unobtrusive and take up minimal header space.
- The picker offers all supported languages minus the user's current target language. The list of available languages must be data-driven (not hard-coded).
- The selected reference language is stored as part of the user's profile.
- Switching the reference language updates all visible UI text, word translations, category names, story descriptions, difficulty labels, host persona descriptions, and progress summaries without requiring a full page reload.

### 3.3 Localisation of UI
- All navigation labels, buttons, headings, instructions, error messages, and informational text must be available in every supported language.
- Switching the reference language must update all visible text without losing navigation context.
- Adding UI translations for a new language must only require adding a new translation file — no code changes to components or routing logic.

### 3.4 Localisation of Content
- Every word entry in the dictionary must have translations in all supported reference languages.
- Word descriptions, phonetic hints, and category names must also be localised.

### 3.5 Supported Languages at Launch

| Language | Code | Target | Reference |
|---|---|---|---|
| Italian | it | ✅ | ✅ |
| Danish | da | ✅ | ✅ |
| English | en | ✅ | ✅ |
| Spanish | es | ✅ | ✅ |

**Planned future languages** (not in current release scope): Swedish, German, Chinese, Icelandic, and others.

Every supported language functions as both a target language and a reference language. Any combination of target + reference is valid as long as they are different languages.

### 3.6 Scalability & Language-as-Data

- The set of supported languages must be defined in a single configuration source (not scattered across conditionals in application code).
- All content-translation storage, retrieval, and display must treat languages generically. Adding a new language must not require adding new `if`/`elif` branches, new model columns, or new per-language field mappings in application code.
- The content model must store translations in a way that scales to 10+ languages without schema changes for each new language.
- All translatable content — category names, word translations, example sentences, story descriptions, host persona descriptions/greetings — must follow the same language-resolution pattern.
- API endpoints must resolve the user's reference language dynamically from the stored translations, without per-language conditional logic in the route handlers.
- When content for the user's reference language is unavailable, the system must fall back to English gracefully with a visual indicator.

### 3.7 Completeness of Reference-Language Content

- Every user-visible text that depends on the reference language must consistently follow the user's selected reference language. This includes but is not limited to:
  - Category names
  - Word translations and example sentences
  - Story descriptions
  - Difficulty level labels
  - Host persona descriptions and greetings
  - Progress summaries and completion indicators
  - Search results and word cards
- No content area may default to a hard-coded language (e.g., English) when the user has selected a different reference language and a translation exists for that language.

## 4. Edge Cases

- If a translation for a specific word is missing in the user's reference language, display the English translation as a fallback with a visual indicator that the translation is approximate.
- If the user has not yet selected a host and is not logged in, default to English as the reference language.
- When a user switches host to a different language, their word progress for the previous target language is preserved and available if they switch back.

## 5. Acceptance Criteria

- [ ] Users can learn pronunciation in Italian, Danish, English, or Spanish by choosing an appropriate host.
- [ ] Reference language can be set independently of target language.
- [ ] UI is fully translated in all supported languages with no untranslated strings.
- [ ] Every word has translations in all supported reference languages.
- [ ] All user-visible content (category names, story descriptions, difficulty labels, host descriptions, progress summaries) consistently follows the user's selected reference language.
- [ ] Both target and reference language preferences persist across sessions.
- [ ] Switching reference language updates all text in place without losing navigation state.
- [ ] English is used as fallback when a translation is missing, with a visual indicator.
- [ ] Progress is preserved per target language when switching hosts.
- [ ] Adding a new language can be achieved by providing content (host personas, seed data, translations, TTS voice assignments, UI translation file) and configuration only — without changes to application logic or database schema restructuring.
- [ ] The backend does not contain per-language conditional branches (if/elif chains) for resolving translations; language resolution is data-driven.
