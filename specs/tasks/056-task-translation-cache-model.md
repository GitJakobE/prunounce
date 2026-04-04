# Task 056: TranslationCache Database Model & Migration

**Feature:** F-OTFLOOKUP (On-the-Fly Word Lookup & Audio)
**Priority:** P1
**Dependencies:** 001 (Backend Scaffolding), 017 (Schema Migration)

## Description

Add a new `TranslationCache` table to the SQLite database to persistently store on-the-fly translation results. This table is separate from the curated `Word` table and stores translations produced by an external translation service when a user clicks a word that is not in the curated dictionary. The table must be created via an Alembic migration.

## Technical Requirements

### Database Model

- New SQLAlchemy model `TranslationCache` in `app/models.py`
- Table name: `TranslationCache`
- Columns:
  - `id` — TEXT primary key, generated via Python `uuid.uuid4()` (consistent with all existing models)
  - `word` — TEXT, NOT NULL, the clicked word in its original normalised form (lowercase)
  - `sourceLang` — TEXT, NOT NULL, the language the word is in (translation-from, i.e. the app's "target language": `it`, `da`, `en`)
  - `targetLang` — TEXT, NOT NULL, the language of the translation (translation-to, i.e. the app's "reference language": `it`, `da`, `en`)
  - `translation` — TEXT, NOT NULL, the translated text
  - `createdAt` — DATETIME, NOT NULL, defaults to current timestamp
- Unique constraint on `(word, sourceLang, targetLang)` — ensures at most one translation per word per language pair
- Index on `(word, sourceLang, targetLang)` for fast lookups

### Naming Convention

- Use the existing camelCase-in-DB / snake_case-in-Python pattern with `mapped_column("camelCaseName", ...)` as used by all other models
- Column names `sourceLang` and `targetLang` use translation-standard nomenclature (source = language being translated FROM, target = language being translated TO). Add a code comment clarifying the mapping to the app's user-facing "target language" and "reference language" terminology.

### Alembic Migration

- Create a new Alembic migration that adds the `TranslationCache` table
- Migration must be idempotent — safe to run against an existing database
- Downgrade must drop the table

## Acceptance Criteria

- [ ] `TranslationCache` model exists in `app/models.py` with all specified columns
- [ ] Unique constraint on `(word, sourceLang, targetLang)` prevents duplicate entries
- [ ] Index on the lookup columns exists for query performance
- [ ] An Alembic migration file creates the table on upgrade and drops it on downgrade
- [ ] The migration runs successfully against the existing database without data loss
- [ ] ID generation uses `uuid.uuid4()` consistent with other models
- [ ] Code comment explains the sourceLang/targetLang terminology mapping

## Testing Requirements

- Model can be instantiated and persisted to the database
- Unique constraint is enforced — inserting a duplicate `(word, sourceLang, targetLang)` raises an integrity error
- Query by `(word, sourceLang, targetLang)` returns the correct record
- Migration upgrade creates the table; downgrade drops it
- Existing tables and data are unaffected by the migration
