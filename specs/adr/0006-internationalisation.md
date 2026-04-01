# ADR-0006: Internationalisation Strategy — i18next (Client) + Column-per-Language (Server)

- **Status:** Accepted (updated: Italian added as a third reference language alongside Danish and English — see [ADR-0010](0010-backend-python-migration.md) and [F-LANG](../features/multi-language-support.md))
- **Date:** 2026-03-16
- **Deciders:** Development team
- **Requirements:** REQ-1 (Multi-language reference support), REQ-2 (Word dictionary), REQ-8 (Example sentences)

## Context and Problem Statement

The application has two distinct internationalisation needs:

1. **UI text** — All labels, buttons, messages, and headings must be available in Danish and English, switchable without page reload.
2. **Content translations** — Every word's translation, category name, and example sentence must exist in both reference languages, served from the database based on the user's preference.

These are fundamentally different problems: UI text is static and bundled with the frontend; content translations are dynamic and stored in the database.

## Decision Drivers

- Two target reference languages (Danish, English) with potential for future additions
- UI text must switch instantly without API calls
- Content translations must be queryable and filterable server-side
- Adding a new reference language should require data entry, not code restructuring
- Consistent developer experience across frontend and backend

## Considered Options

### Option 1: i18next + column-per-language in the database (Chosen)

Use react-i18next for UI text with JSON translation files bundled in the frontend. Store content translations as separate columns in the database (e.g., `translationEn`, `translationDa`, `nameEn`, `nameDa`). The API selects the appropriate column based on the `lang` query parameter and returns it as a generic `translation` field.

### Option 2: i18next for everything (UI + content via API-backed translations)

Store all translations (including word data) in i18next's resource format and load them dynamically. This would unify the translation mechanism but requires transforming the word database into i18next-compatible resources, which is awkward for structured data that includes metadata (phonetic hints, difficulty, audio paths).

### Option 3: Database-only translations (no frontend i18n library)

Store all text — including UI labels — in the database and fetch them via API. This centralises all translations but introduces API latency for every UI string, making language switching slow and offline-unfriendly.

### Option 4: Separate translation table (normalised)

Instead of column-per-language, use a `Translation` table with `(entityId, language, field, value)` rows. Fully normalised and supports unlimited languages without schema changes. However, queries become complex (multiple joins per word), and for two languages the normalisation overhead isn't justified.

## Decision Outcome

**Chosen: Option 1 — i18next for UI text, column-per-language for content**

### Implementation Details

**Frontend (i18next):**
- Translation files: `src/frontend/src/i18n/en.json` and `da.json`
- Namespace-free, flat key structure (e.g., `auth.login`, `categories.title`, `words.example`)
- `useTranslation()` hook in components for reactive language switching
- Language defaults to browser locale, overridden by user profile preference on login
- Switching language calls `i18n.changeLanguage()` — all visible text updates without re-render of the route

**Backend (column-per-language):**
- Word model: `translationEn`, `translationDa`, `exampleEn`, `exampleDa`
- Category model: `nameEn`, `nameDa`
- API routes accept `?lang=en|da` and map to the appropriate column
- Response uses generic field names (`translation`, `name`, `example`) — the frontend doesn't know about column names

### Consequences

**Positive:**
- UI text switching is instant — no API calls, no flicker
- Content translations are simple to query — direct column access, no joins
- The API response is language-agnostic: `{ translation: "bread" }` regardless of which column it came from
- Adding translations for a new word is a single seed file entry with all language columns
- i18next's interpolation (`{{count}}`) handles pluralisation and dynamic values

**Negative:**
- Adding a third reference language requires a schema migration (new columns) and a Prisma migration — but this is a known, one-time operation per language
- Duplicated column pattern (`*En`, `*Da`) across Word, Category, and example fields — manageable at 2 languages but would become unwieldy at 5+
- UI translation files must be kept in sync manually — no compile-time check for missing keys

**Neutral:**
- The language switcher component is always visible in the header, accessible from every page (REQ-1)
- The user's language preference is persisted in the User model and applied on login
