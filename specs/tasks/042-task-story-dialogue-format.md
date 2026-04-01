# Task 042: Story Dialogue Body Format & Data Model

**Feature:** F-DIALOGUE (Story Dialogue Formatting)
**Priority:** P1
**Dependencies:** 029 (Story Data Model & API), 030 (Story Seed Data)

## Description

Define and implement a dialogue markup convention within the existing `Story.body` text field so conversational stories can encode speaker attribution per line. Add a `format` column to the Story model to distinguish narrative stories from dialogue stories. This task establishes the data layer only — no frontend or API response changes.

## Technical Requirements

### Dialogue Markup Convention

- Dialogue lines in the `body` field use the format: `SPEAKER_LABEL: Spoken text.`
- Each dialogue line is separated by a newline character (`\n`).
- The colon-space (`: `) separator between speaker label and text is the canonical delimiter.
- Narrative paragraphs (scene-setting, stage directions) use a blank line (`\n\n`) separator and have no speaker prefix.
- Speaker labels:
  - Must be 1–30 characters, containing only letters, spaces, and accented characters.
  - Must be consistent within a story (same label for the same character throughout).
  - Are in the target language of the story (e.g., "Marco", "Cameriere", "Dottoressa").

### Example Body Format

```
Marco entra nel bar.

Marco: Buongiorno! Vorrei un caffè, per favore.
Barista: Certo, subito. Vuole anche qualcosa da mangiare?
Marco: Sì, un cornetto, grazie.
Barista: Benissimo. Desidera zucchero nel caffè?
Marco: No, grazie, lo prendo amaro.
```

### Data Model Changes

- Add a `format` column to the `Story` table:
  - Type: `String`, nullable: `False`, default: `"narrative"`
  - Allowed values: `"narrative"`, `"dialogue"`, `"mixed"`
  - `narrative` — body is plain prose paragraphs (existing behaviour)
  - `dialogue` — body is entirely speaker-attributed dialogue lines
  - `mixed` — body contains both narrative paragraphs and dialogue lines
- Add a `speakers` column to the `Story` table:
  - Type: `String`, nullable: `True`, default: `None`
  - Stores a JSON-encoded list of speaker labels used in the story (e.g., `["Marco", "Barista"]`)
  - Populated during seeding; `None` for narrative stories
- Create a database migration for the new columns with safe defaults (all existing stories default to `"narrative"` format and `None` speakers until seed data is updated)

### Parsing Utility

- Implement a Python utility function `parse_dialogue_body(body: str, format: str)` that:
  - For `"narrative"` format: returns the body as-is (list of paragraph strings)
  - For `"dialogue"` or `"mixed"` format: returns a structured list of segments, each being either:
    - `{"type": "narration", "text": "..."}` — a narrative paragraph
    - `{"type": "dialogue", "speaker": "Marco", "text": "..."}` — a dialogue line
  - This utility is used by the API to return structured body content for the frontend

### Validation Rules

- A dialogue-format story must have at least 2 distinct speakers.
- A dialogue-format story must have no more than 4 speakers.
- Every line prefixed with `LABEL:` must use a label declared in the `speakers` list.
- A mixed-format story must contain at least one narrative paragraph and at least one dialogue line.

## Acceptance Criteria

- [ ] `format` column added to Story table with default `"narrative"`
- [ ] `speakers` column added to Story table, nullable
- [ ] Database migration applies cleanly to existing data
- [ ] Existing stories continue to work unchanged (default `narrative` format)
- [ ] `parse_dialogue_body()` correctly parses narrative, dialogue, and mixed formats
- [ ] Validation rules enforce speaker count and label consistency
- [ ] Utility correctly strips speaker labels from text while preserving them as metadata

## Testing Requirements

- Parse a pure narrative body → returns list of paragraph strings
- Parse a pure dialogue body → returns structured segments with speaker attribution
- Parse a mixed body → returns interleaved narration and dialogue segments
- Validation rejects dialogue story with fewer than 2 speakers
- Validation rejects dialogue story with more than 4 speakers
- Validation rejects dialogue line with undeclared speaker label
- Migration preserves existing story data with correct defaults
