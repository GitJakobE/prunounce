# Task 017: Database Schema Migration — Multi-Language Word Model

**Feature:** F-DICT (Word Dictionary), F-LANG (Multi-Language Learning)
**Priority:** P0
**Dependencies:** 001 (Backend Scaffolding), existing schema baseline (tasks 001–016 complete)

## Description

Migrate the database schema from a single-language (Italian-only) word model to a multi-language model. The current schema has hardcoded `italian`, `translationEn`, `translationDa` columns. The new schema must support words in any target language (Italian, Danish, English), with translations in all other supported languages. The schema must also support user-contributed words.

## Technical Requirements

### Word Model Changes
- Replace the single `italian` column with a `word` column (the word in its target language)
- Add a `language` column to the Word model indicating which target language this word belongs to (`"it"`, `"da"`, `"en"`)
- Add a `translationIt` column alongside existing `translationEn` and `translationDa` columns
- Add `exampleIt` column should remain (as it currently stores the target-language example for Italian words — repurpose it to always hold the target-language example)
- Rename current `exampleIt` to be the target-language example field, or add a generic `exampleTarget` field
- Add a `source` column to indicate word origin: `"seed"` or `"user"`
- Add a `contributedBy` nullable column referencing the User who contributed the word (null for seeded words)
- Change the unique constraint from `italian` to a composite unique on `[word, language]`

### Category Model Changes
- Add a `nameIt` column for Italian-language category names

### UserProgress Changes
- No structural changes needed — progress is already per word, and words are per language, so progress is implicitly per language

### Migration Strategy
- Create a Prisma migration that:
  1. Adds the new columns with defaults
  2. Copies data from `italian` → `word` for existing entries
  3. Sets `language` to `"it"` for all existing words
  4. Sets `source` to `"seed"` for all existing words
  5. Drops the old `italian` column
  6. Updates the unique constraint

## Acceptance Criteria

- [ ] Migration applies cleanly on top of the existing database
- [ ] All existing Italian words are preserved with `language = "it"`
- [ ] The `word` column replaces the `italian` column
- [ ] A `language` column exists with values `"it"`, `"da"`, or `"en"`
- [ ] Translation columns exist for all three languages (En, Da, It)
- [ ] A `source` column distinguishes seeded vs user-contributed words
- [ ] A `contributedBy` column references the contributing user (nullable)
- [ ] Unique constraint is on `[word, language]`
- [ ] Category model has `nameIt` column
- [ ] Prisma client regenerates with the new types
- [ ] All existing backend code (routes, services) is updated to use the new column names
- [ ] All existing tests pass after the migration

## Testing Requirements

- Migration applies without errors on an existing database with data
- Prisma generate produces a typed client with the new fields
- Existing seed data is preserved after migration
- Unique constraint prevents duplicate words within the same language
- Unique constraint allows the same word text in different languages
