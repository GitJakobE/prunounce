# Task 030: Story Seed Data

**Feature:** F-STORY (Story Reading)
**Priority:** P1
**Dependencies:** 029 (Story Data Model & API)

## Description

Create seed data for stories across all three target languages (Italian, Danish, English) and three difficulty levels (beginner, intermediate, advanced). Stories must be age-appropriate, culturally relevant short texts suitable for language learners. The seeder must follow the existing idempotent seeding pattern in `seed_data.py`.

## Technical Requirements

### Seed Data Files

- Create `src/backend/data/stories.json` following the same pattern as existing seed data files
- Provide 27 stories total: 9 per language × 3 difficulty levels (3 stories per difficulty per language)
- Each story object must include: `id`, `slug`, `language`, `difficulty`, `title`, `descriptionEn`, `descriptionDa`, `descriptionIt`, `body`, `order`

### Difficulty Guidelines

- **Beginner:** 50–100 words, simple present tense, common vocabulary, short sentences
- **Intermediate:** 150–250 words, mixed tenses, broader vocabulary, compound sentences
- **Advanced:** 300–500 words, complex grammar, idiomatic expressions, varied sentence structures

### Content Guidelines

- Stories should be original, educational, and culturally relevant to the target language
- Topics: daily life, travel, food, culture, greetings, shopping, directions, weather, family
- Each story must be self-contained (no multi-part series)
- Avoid copyrighted or sensitive content

### Seeder Integration

- Extend `seed_data.py` to import and upsert stories from `stories.json`
- Use the same idempotent upsert pattern: skip if a story with the same `(slug, language)` already exists
- Maintain ordering: seed stories after categories and words (stories may reference vocabulary)

## Acceptance Criteria

- [ ] `stories.json` contains 27 stories (9 per language, 3 per difficulty per language)
- [ ] All stories have valid `slug`, `language`, `difficulty`, `title`, descriptions, `body`, and `order`
- [ ] Beginner stories are 50–100 words, intermediate 150–250, advanced 300–500
- [ ] `seed_data.py` seeds stories idempotently (re-running does not create duplicates)
- [ ] Stories are seeded after categories and words
- [ ] All story slugs are URL-friendly (lowercase, hyphens, no special characters)
- [ ] Each `(slug, language)` pair is unique

## Testing Requirements

- Seeder creates all 27 stories on first run
- Re-running seeder does not duplicate stories
- All stories satisfy word count constraints for their difficulty level
- All slugs are valid URL-friendly strings
- All language codes are valid (`it`, `da`, `en`)
- All difficulty levels are valid (`beginner`, `intermediate`, `advanced`)
