# Task 043: Reformat Story Seed Data with Dialogue Markup

**Feature:** F-DIALOGUE (Story Dialogue Formatting)
**Priority:** P1
**Dependencies:** 042 (Story Dialogue Body Format & Data Model)

## Description

Rewrite all 27 story bodies in `seed_stories.py` to use the dialogue markup convention defined in Task 042. Each conversational story must have named speaker labels, proper line-by-line attribution, and the `format` and `speakers` fields populated. This is a content authoring task — every story must be reviewed for grammatical correctness and natural phrasing during the rewrite.

## Technical Requirements

### Content Conversion

- Convert all 27 stories from flat concatenated text to the `SPEAKER: text` dialogue format
- Each story must have culturally appropriate character names in the target language
- Assign 2–3 named characters per story (maximum 4)
- Speaker labels should be first names or role titles (e.g., "Marco", "Barista", "Dottoressa") — whichever is clearest for the scenario
- Populate the `format` field: set to `"dialogue"` for all current stories (all are pure conversation)
- Populate the `speakers` field: JSON list of speaker labels (e.g., `["Marco", "Barista"]`)

### Speaker Assignment Guidelines by Story

**Italian stories:**
- `it-beginner-cafe` — Cliente, Barista
- `it-beginner-mercato` — Cliente, Venditore
- `it-beginner-presentazione` — Marco, Sofia
- `it-intermediate-ristorante` — Cameriere, [group guests — use 2 speaker labels]
- `it-intermediate-medico` — Paziente, Dottoressa
- `it-intermediate-treno` — Viaggiatore, Bigliettaio
- `it-advanced-banca` — Cliente, Impiegato
- `it-advanced-affitto` — Inquilino, Proprietario
- `it-advanced-colloquio` — Candidato, Intervistatore

**Danish stories:**
- Assign equivalent Danish role labels (e.g., "Kunde", "Barista", "Læge", "Patient")

**English stories:**
- Assign equivalent English role labels (e.g., "Customer", "Barista", "Doctor", "Patient")

### Grammar and Content Review

- During the rewrite, review and correct any grammatical errors in the original text
- Fix spelling mistakes and incorrect word usage
- Ensure natural phrasing appropriate to the story's difficulty level
- Ensure each line is a self-contained speaker turn (no mid-sentence speaker switches)
- Preserve the original conversational flow and topic

### Seed Function Updates

- Update `seed_stories.py` to include `format` and `speakers` fields in each story dict
- Seeder must handle the upsert of new `format` and `speakers` columns
- Re-running the seeder must update existing stories with the new format without creating duplicates

## Acceptance Criteria

- [ ] All 27 stories converted to `SPEAKER: text` dialogue format
- [ ] Each story has 2–4 named speakers with culturally appropriate labels
- [ ] `format` field set to `"dialogue"` for all stories
- [ ] `speakers` field populated with JSON list of speaker labels
- [ ] Grammar and spelling reviewed and corrected in all 27 stories
- [ ] Story bodies use `\n` line separators between dialogue turns
- [ ] Seeder upserts updated stories without creating duplicates
- [ ] All stories pass the dialogue validation rules from Task 042
- [ ] Word count remains within difficulty-level guidelines after reformatting

## Testing Requirements

- All 27 stories pass dialogue format validation (speaker count, label consistency)
- Seeder creates stories with correct `format` and `speakers` values
- Re-running seeder does not create duplicate stories
- Each story body parses correctly with `parse_dialogue_body()`
- Word counts remain within acceptable ranges for each difficulty level
- No story has more than 4 speakers
- Every dialogue line has a recognised speaker label
