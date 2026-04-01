# Task 020: Danish & English Seed Data

**Feature:** F-DICT (Word Dictionary)
**Priority:** P0
**Dependencies:** 017 (Schema Migration)

## Description

Create seed data files for Danish and English word dictionaries, matching the structure and scope of the existing Italian seed data. Each language needs 250+ words across 10+ categories and 3 difficulty levels, with translations in all supported reference languages and example sentences.

## Technical Requirements

### Danish Seed Data
- A seed file containing 250+ Danish words
- Each word includes: Danish word, phonetic hint (for non-Danish speakers), translations in English and Italian, difficulty level, category assignments, example sentence in Danish with translations in English and Italian
- Words should cover the same 10+ categories as the Italian dictionary
- Balanced distribution across Beginner, Intermediate, and Advanced difficulty levels

### English Seed Data
- A seed file containing 250+ English words
- Each word includes: English word, phonetic hint (for non-English speakers), translations in Danish and Italian, difficulty level, category assignments, example sentence in English with translations in Danish and Italian
- Words should cover the same 10+ categories as the Italian dictionary
- Balanced distribution across difficulty levels

### Italian Seed Data Updates
- Update the existing Italian seed file to include Italian translations (the `translationIt` column, which may be the same as the word itself or a gloss)
- Ensure all Italian words have a value in the `translationIt` column

### Category Italian Names
- Add Italian names (nameIt) for all existing categories in the seed data

### Seed Script Updates
- Update the seed script to:
  - Accept a language parameter or seed all languages
  - Set the `language` field on each word entry
  - Set `source = "seed"` for all seeded entries
  - Handle the new `word` column (replacing `italian`)
  - Upsert using the composite `[word, language]` unique constraint
  - Populate category `nameIt` values

## Acceptance Criteria

- [ ] Danish seed file contains 250+ unique words
- [ ] English seed file contains 250+ unique words
- [ ] All words have translations in all three languages
- [ ] All words have phonetic hints
- [ ] All words have difficulty assignments
- [ ] All words have example sentences with translations in all three languages
- [ ] All words belong to at least one category
- [ ] All categories have Italian names (nameIt)
- [ ] Seed script populates all three language word sets
- [ ] Seed script is idempotent across all languages
- [ ] Running seed twice produces no duplicates

## Testing Requirements

- Seed completes without errors for all three languages
- Seed is idempotent: running twice yields the same row count per language
- Each language has words in all categories
- Each language has words at all difficulty levels
- All words have non-empty translations in all three reference languages
