# ADR-0028: Internationalisation Scalability — Normalised Translation Table

- **Status:** Proposed
- **Date:** 2026-04-05
- **Deciders:** Development team
- **Requirements:** REQ-1 (Multi-language learning), F-LANG (Multi-Language Support)
- **Supersedes:** [ADR-0006](0006-internationalisation.md) (server-side column-per-language approach only; i18next for UI text is retained)
- **Related:** [ADR-0010](0010-backend-python-migration.md), [ADR-0017](0017-content-seeding.md)

## Context and Problem Statement

ADR-0006 chose a column-per-language approach for content translations: each translatable field gets one database column per language (e.g., `translation_en`, `translation_da`, `translation_it`, `translation_es`). This was pragmatic when only two languages existed, but the PRD now requires four reference languages at launch (English, Danish, Italian, Spanish) and explicitly mandates that **adding a new language must not require application logic or database schema changes** — only new content and configuration.

The column-per-language approach violates this requirement: every new language demands an Alembic migration adding columns to `Word`, `Category`, and any other translatable table. The number of columns grows multiplicatively (translatable fields × languages). With 4 languages and fields for translation, example, example translation, and category name, the schema already has 16+ language-specific columns. Adding a fifth language means another migration adding 4+ columns.

The PRD's language scalability mandate is a first-class requirement, not an aspirational stretch goal. The architecture must support adding languages such as Icelandic and Swedish through content alone.

## Decision Drivers

- PRD REQ-1 mandates adding languages without schema changes or code modifications
- Currently 4 languages with explicit plans for more (Icelandic, Swedish mentioned)
- Column proliferation makes the schema harder to understand and maintain
- Seed data and API logic must map column names per language — brittle and error-prone
- UI text (i18next with JSON files) already scales well and is not affected by this change
- The solution must not degrade query performance for the common case (fetching a single language's translations)

## Considered Options

### Option 1: Normalised translation table (Chosen)

Replace all `*_en`, `*_da`, `*_it`, `*_es` columns with a single `ContentTranslation` table:

```
ContentTranslation
  id            INTEGER PRIMARY KEY
  entity_type   TEXT NOT NULL        -- 'word', 'category', 'story', etc.
  entity_id     INTEGER NOT NULL     -- FK to the source entity
  language      TEXT NOT NULL         -- ISO 639-1 code: 'en', 'da', 'it', 'es', ...
  field         TEXT NOT NULL         -- 'translation', 'example', 'name', 'description', etc.
  value         TEXT NOT NULL

  UNIQUE(entity_type, entity_id, language, field)
  INDEX(entity_type, entity_id, language)
```

The API retrieves translations with a single query filtered by `entity_type`, `entity_id`, and `language`. Adding a new language is purely an INSERT operation — no schema migration.

### Option 2: Keep column-per-language, accept migrations

Continue with the current approach. Each new language triggers an Alembic migration adding columns. Accept that "no schema changes" is aspirational rather than enforced.

**Pros:**
- No migration of existing data
- Simple column access remains fast
- No query complexity increase

**Cons:**
- **Directly violates** the PRD's language scalability requirement (REQ-1)
- Column count grows as `translatable_fields × languages` — already 16+ columns, heading toward 20+ with a fifth language
- Every new language requires coordinated changes: migration, model update, API column mapping, seed script update
- Schema becomes progressively harder to read and maintain

### Option 3: JSON column per entity for translations

Store translations as a JSON blob on each entity: `translations JSON` containing `{"en": {"translation": "bread", "example": "..."}, "da": {...}}`.

**Pros:**
- No schema changes to add languages
- All translations for an entity in one place
- SQLite supports JSON functions for querying

**Cons:**
- Cannot index individual language values efficiently
- JSON querying in SQLite is less performant than column/table access
- Validation of translation completeness requires parsing JSON rather than checking column nullability
- Partial updates (changing one language's translation) require JSON manipulation
- Loses relational integrity — no foreign key constraints on language codes

### Option 4: Hybrid — translation table for words, columns for categories

Use a normalised table only for the high-volume `Word` translations while keeping column-per-language for low-volume entities like `Category` (only ~12 categories).

**Pros:**
- Reduces migration burden for the largest table
- Categories rarely change and have few rows

**Cons:**
- Two different translation patterns in the same codebase — inconsistent and confusing
- Categories still need migrations when adding a language
- Still violates the "no schema changes" requirement, just less frequently

## Decision Outcome

**Chosen: Option 1 — Normalised translation table**

### Migration Strategy

1. Create the `ContentTranslation` table
2. Migrate existing column data into rows (one-time data migration script)
3. Drop the language-specific columns from `Word`, `Category`, and other entities
4. Update the SQLAlchemy models to use a relationship to `ContentTranslation`
5. Update API endpoints to query translations via the new table
6. Update seed scripts to insert translations as rows rather than columns

### API Changes

The API continues to accept `?lang=en` and return generic field names (`translation`, `example`, `name`). The change is internal — the backend queries the `ContentTranslation` table instead of selecting a language-specific column. The frontend is unaffected.

```python
# Before (column-per-language):
word.translation_en

# After (normalised):
db.query(ContentTranslation).filter_by(
    entity_type='word', entity_id=word.id, language='en', field='translation'
).first().value
```

For performance, a helper method on the model can batch-load all translations for a language in a single query when listing words:

```python
translations = db.query(ContentTranslation).filter(
    ContentTranslation.entity_type == 'word',
    ContentTranslation.entity_id.in_(word_ids),
    ContentTranslation.language == lang
).all()
```

### Adding a New Language

With this approach, adding a new language (e.g., Swedish `sv`) requires:

1. Add UI translation file: `src/frontend/src/i18n/sv.json`
2. Add `sv` to the supported languages configuration
3. Insert `ContentTranslation` rows for all existing entities with `language='sv'`
4. Create host personas for Swedish
5. Assign TTS voices for Swedish

**No Alembic migration. No model changes. No API code changes.**

### Performance Considerations

- The `UNIQUE(entity_type, entity_id, language, field)` index ensures fast lookups
- The additional `INDEX(entity_type, entity_id, language)` supports batch loading all fields for an entity+language pair
- For listing pages (e.g., word list), a single query with `IN` clause retrieves all translations, avoiding N+1
- SQLite handles this pattern efficiently for the expected data volume (< 10,000 word entries × 5 languages × 4 fields = ~200,000 rows)

## Consequences

**Positive:**
- Fully satisfies the PRD's "no schema changes to add a language" requirement
- Language list becomes data-driven — defined in configuration, not in the schema
- Cleaner entity tables — `Word` has only language-independent fields (word text, phonetic hint, difficulty, category FK)
- Seed data format simplifies: translations are a nested structure rather than flat columns
- The pattern generalises to any new translatable entity (e.g., story descriptions, achievement names)

**Negative:**
- One-time migration effort to move existing data from columns to rows
- Slightly more complex queries (join or subquery vs direct column access)
- Translation completeness checks require a query rather than checking column nullability
- Bulk operations (seeding) insert more rows than before

**Neutral:**
- Frontend i18next approach is unchanged — this ADR affects only server-side content translations
- The API contract (response shape) is unchanged — this is a backend-internal refactor
- Fallback logic (missing translation → English) translates to: "if no row for requested language, query for `language='en'`"
