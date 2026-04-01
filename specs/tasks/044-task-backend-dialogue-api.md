# Task 044: Backend Story API — Dialogue Metadata & Structured Body

**Feature:** F-DIALOGUE (Story Dialogue Formatting)
**Priority:** P1
**Dependencies:** 042 (Story Dialogue Body Format), 043 (Seed Data Rewrite)

## Description

Update the story API endpoints to return dialogue metadata and a structured body representation so the frontend can render dialogue and narrative stories differently. The story list endpoint gains a `format` field; the story detail endpoint returns a parsed body with speaker attribution.

## Technical Requirements

### Updated API Response Schemas

#### Story List (`GET /api/stories`)

Add to `StoryListItem`:
- `format: str` — `"narrative"`, `"dialogue"`, or `"mixed"`
- `speakers: list[str] | None` — list of speaker labels, or `null` for narrative stories

#### Story Detail (`GET /api/stories/{story_id}`)

Update `StoryDetailResponse`:
- `format: str` — same as above
- `speakers: list[str] | None` — same as above
- `body: str` — keep the raw body text (for backward compatibility and narration)
- `segments: list[Segment]` — new field: the parsed body as a list of structured segments

Each `Segment` is one of:
```json
{ "type": "narration", "text": "Marco entra nel bar." }
```
or:
```json
{ "type": "dialogue", "speaker": "Marco", "text": "Buongiorno! Vorrei un caffè, per favore." }
```

### Response Schema Definitions

- Define new Pydantic models: `StorySegment` (with discriminated `type` field), `StoryDetailResponse` (extended)
- `StorySegment` must validate that dialogue segments have a non-empty `speaker` field
- `StorySegment` must validate that narration segments have no `speaker` field

### API Logic Changes

- In the story detail endpoint, call `parse_dialogue_body(story.body, story.format)` to produce the `segments` list
- In the story list endpoint, include `format` and `speakers` from the database columns
- The `speakers` column is stored as a JSON string in the database — deserialise it to a Python list before returning

### Backward Compatibility

- The raw `body` field remains in the detail response for clients that don't understand segments (e.g., narration TTS still uses raw body)
- Narrative-format stories return `segments` as a single narration segment containing the full body text
- Existing API consumers that ignore `format`, `speakers`, and `segments` continue to work

## Acceptance Criteria

- [ ] Story list response includes `format` and `speakers` for each story
- [ ] Story detail response includes `segments` with parsed dialogue/narration structure
- [ ] Narrative stories return a single narration segment in `segments`
- [ ] Dialogue stories return properly attributed dialogue segments
- [ ] Mixed stories return interleaved narration and dialogue segments
- [ ] Raw `body` field still present in detail response for backward compatibility
- [ ] `speakers` is deserialised from JSON string to list in API response
- [ ] Response validation enforces correct segment structure

## Testing Requirements

- Story list for dialogue stories includes `format: "dialogue"` and non-empty `speakers` list
- Story list for narrative stories includes `format: "narrative"` and `speakers: null`
- Story detail for dialogue story returns correct segment count and speaker attribution
- Story detail for narrative story returns single narration segment
- Story detail for mixed story returns correct interleaving of segment types
- Raw `body` field is still present alongside `segments`
- Invalid segment structure (e.g., dialogue without speaker) is rejected by schema validation
