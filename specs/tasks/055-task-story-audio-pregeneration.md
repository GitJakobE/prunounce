# Task 055: Story Audio Pre-Generation & Backfill

**Feature:** F-STORY (Story Reading)
**Priority:** P1
**Dependencies:** 029 (Story Data Model & API), 030 (Story Seed Data), 046 (Dialogue TTS Narration)

## Description

All story audio must be pre-generated and persisted in the database at seeding time rather than generated on demand. The system must support idempotent backfill — re-running the process should skip stories whose content and voice configuration have not changed, and only generate audio for new or modified entries. The pipeline must handle transient TTS provider failures gracefully through automatic retry with exponential backoff.

## Functional Requirements

### Pre-Generation During Seeding

- After all story text records are seeded, the seeder must iterate every persisted story and generate audio for all supported playback speeds
- The five supported speeds are: very slow, slow, normal, fast, and very fast
- Each story × speed combination produces one audio file stored as a database record
- For a baseline of 81 stories (27 per language × 3 lengths), this yields 405 audio records

### Idempotent Backfill

- Each audio record must store a content hash derived from story metadata (language, length, format, title, body, speakers) and the voice configuration used
- On re-run, the system must compare the current content hash against the stored hash and skip generation if they match
- If content or voice configuration has changed (e.g. story body was edited, or the voice pool was updated), the existing record must be overwritten with freshly generated audio
- A versioning token must be included in the hash so that changes to the generation logic itself trigger regeneration

### Retry & Resilience

- TTS generation must retry on transient failures (network errors, HTTP 503, connection drops)
- The retry strategy must use exponential backoff with at least four attempts
- Individual story failures must not abort the entire batch — the seeder must continue with remaining stories and report a failure count at the end
- A second run of the seeder must fill in any records that failed on the previous attempt

### Multi-Voice Dialogue Audio

- Dialogue-format stories must be generated with distinct voices per speaker (not a single voice for the entire story)
- Speaker labels (e.g. "Cliente:", "Barista:") must be stripped from the audio — only the spoken text is synthesized
- Each speaker must be assigned a consistent voice for the duration of the story
- Voice assignment must draw from a per-language voice pool so that the same speaker always gets the same voice within a story

### Serving Pre-Generated Audio

- The story audio API endpoint must serve audio exclusively from the persisted database records
- If a requested story × speed combination has no pre-generated record, the endpoint must return an appropriate error indicating the audio is unavailable (not silently generate on demand)
- Response headers must indicate the audio is immutable/cacheable since it does not change between requests

## Acceptance Criteria

- [ ] Running the seeder generates audio records for every story × speed combination
- [ ] Re-running the seeder with unchanged content skips all existing records (no redundant TTS calls)
- [ ] Editing a story's body and re-running the seeder regenerates only that story's audio
- [ ] Transient TTS failures are retried with backoff (at least four attempts per segment)
- [ ] Individual failures do not abort the batch — remaining stories are still processed
- [ ] A follow-up seeder run fills in any records that failed on the prior run
- [ ] Dialogue stories use distinct voices per speaker
- [ ] Speaker labels are not audible in the generated audio
- [ ] The audio API endpoint returns pre-generated audio from the database
- [ ] The audio API endpoint returns an error status when audio has not been pre-generated
- [ ] Total pre-generated record count matches (number of stories) × (number of speeds)

## Testing Requirements

- Seeder creates audio records for all stories at all speeds
- Re-running seeder with unchanged data performs zero TTS calls (verified via content hash match)
- Modifying a story's body causes regeneration of that story's audio only
- A simulated TTS failure for one story does not prevent other stories from being generated
- Dialogue audio output contains no speaker label text
- Dialogue audio uses different voices for different speakers in the same story
- API endpoint serves correct audio bytes and MIME type from the database
- API endpoint returns error status for missing audio records
