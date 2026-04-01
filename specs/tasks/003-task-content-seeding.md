# Task 003: Content Seeding

**Feature:** F-DICT (Word Dictionary & Categories)
**Priority:** P0
**Dependencies:** 001 (Backend Scaffolding)
**ADRs:** ADR-0003 (Database), ADR-0006 (Internationalisation)

## Description

Create the structured seed data file containing the full word dictionary and implement the idempotent seed script. The seed data must include all categories, words with translations in both reference languages, phonetic hints, difficulty levels, and example sentences.

## Technical Requirements

- Seed data file (JSON) containing:
  - At least 10 thematic categories with English and Danish names
  - At least 184 words, each with: Italian word, phonetic hint, English translation, Danish translation, difficulty level (beginner/intermediate/advanced), category assignment(s), example sentences in Italian/English/Danish
- Seed script (`seed.ts`) that:
  - Reads the JSON seed file
  - Creates categories with `upsert` (idempotent)
  - Creates words with `upsert` on the Italian word (idempotent)
  - Creates word-category associations
  - Can be run via `npm run db:seed`
- Example sentences data file (`examples.json`) with Italian, English, and Danish example sentences for each word

## Acceptance Criteria

- [ ] Seed file contains at least 10 categories
- [ ] Seed file contains at least 184 unique Italian words
- [ ] Every word has translations in both English and Danish
- [ ] Every word has a phonetic hint
- [ ] Every word has a difficulty level assignment
- [ ] Every word has an Italian example sentence with English and Danish translations
- [ ] `npm run db:seed` populates the database successfully
- [ ] Running `npm run db:seed` a second time does not create duplicates
- [ ] All categories have words across at least two difficulty levels

## Testing Requirements

- Seed script completes without errors on an empty database
- Seed script is idempotent: running twice produces the same row count
- All words have non-empty translations in both languages
- All words belong to at least one category
