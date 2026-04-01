# Task 031: Story Narration TTS Service

**Feature:** F-STORY (Story Reading)
**Priority:** P1
**Dependencies:** 029 (Story Data Model & API), 006 (Backend Audio)

## Description

Implement streaming text-to-speech narration for stories using Edge TTS. Unlike single-word audio (which is pre-cached per host), story narration is generated on demand and streamed to the client. The service must support five playback speeds via SSML `<prosody rate>` control and return word boundary timing data to enable karaoke-style highlighting in the frontend.

## Technical Requirements

### Narration Endpoint

- `GET /api/stories/:storyId/narrate` — stream audio narration of the story body
  - Query parameters:
    - `hostId` — the host persona whose voice to use (required)
    - `speed` — one of `0.5`, `0.75`, `1.0`, `1.25`, `1.5` (default: `1.0`)
  - Returns `audio/mpeg` streamed response
  - Protected by auth middleware
  - Returns 404 if story not found

### Word Boundary Timing Endpoint

- `GET /api/stories/:storyId/timing` — return word boundary events for the story
  - Query parameters:
    - `hostId` — the host persona whose voice to use (required)
    - `speed` — one of `0.5`, `0.75`, `1.0`, `1.25`, `1.5` (default: `1.0`)
  - Returns JSON array of `{ word, offset, duration }` objects
  - `offset` and `duration` are in milliseconds
  - Protected by auth middleware

### TTS Service Extension

- Extend `EdgeTTSProvider` with a `stream_story()` method that:
  - Accepts full story body text, host voice name, and speed parameter
  - Wraps text in SSML `<prosody rate="X">` element where X maps to the speed parameter
  - Uses `edge_tts.Communicate` with `--boundary-type word` to capture word boundary events
  - Yields audio chunks for streaming response
  - Collects and returns word boundary timing data

### Speed Mapping

| Speed Parameter | SSML Rate | Label       |
|-----------------|-----------|-------------|
| `0.5`           | `-50%`    | Very Slow   |
| `0.75`          | `-25%`    | Slow        |
| `1.0`           | `+0%`     | Normal      |
| `1.25`          | `+25%`    | Fast        |
| `1.5`           | `+50%`    | Very Fast   |

### Caching Strategy

- Story narration is NOT pre-cached (unlike single-word audio)
- Narration is generated on demand per request
- Word boundary timing MAY be cached in-memory (keyed by storyId + hostId + speed) to avoid regenerating timing data on repeated requests

## Acceptance Criteria

- [ ] `GET /api/stories/:storyId/narrate` streams audio for the story body
- [ ] Audio uses the correct host persona's voice
- [ ] All five speed values produce correctly paced audio via SSML prosody
- [ ] Invalid speed values are rejected with 400
- [ ] `GET /api/stories/:storyId/timing` returns word boundary timing as JSON
- [ ] Timing data includes word text, offset (ms), and duration (ms)
- [ ] 404 is returned for non-existent stories
- [ ] 401 is returned for unauthenticated requests
- [ ] Invalid hostId returns 400

## Testing Requirements

- Narration endpoint returns audio/mpeg content type
- Narration uses the correct voice for the specified host
- Each speed parameter produces audio with the correct SSML prosody rate
- Invalid speed parameter returns 400
- Timing endpoint returns valid JSON with word, offset, duration fields
- Timing entries cover all words in the story body
- Non-existent story returns 404
- Unauthenticated request returns 401
- Invalid hostId returns 400
