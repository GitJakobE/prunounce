# Task 021: Multi-Language Audio Service

**Feature:** F-AUDIO (Audio Pronunciation)
**Priority:** P0
**Dependencies:** 017 (Schema Migration), 018 (Expand Hosts)

## Description

Update the TTS audio service and audio API endpoints to generate and serve pronunciation audio in the user's target language using the appropriate host voice. Currently the service only generates Italian audio. After this task, it generates audio in Italian, Danish, or English using the host's assigned neural voice.

## Technical Requirements

### TTS Service Changes
- The `getAudioPath()` function must accept the word text, target language, and host voice name
- Audio caching must include the language in the cache key to prevent collisions (e.g., a Danish word "tak" and an Italian word "tac" must not share a cache file)
- Cache filename pattern: `{sanitizedWord}_{hostId}.mp3` (existing pattern already includes hostId, which implicitly includes language since each host has one language)

### Audio Route Changes
- `GET /api/audio/:wordId` — resolve the word's language from the Word record, resolve the host's voice from the user's profile, generate/serve audio in the correct language
- `GET /api/audio/:wordId/example` — same logic but for the example sentence
- Validate that the word's language matches the user's target language (prevent serving audio for a word in a different language than the user is learning)

### Voice Verification
- Verify all 12 host voices (4 Italian, 4 Danish, 4 English) can generate audio via msedge-tts
- Test at least one word in each language with each voice

### Error Handling
- If a word has no text in the target language (edge case for partially translated UGC), return a clear error
- If the TTS service fails, return a user-friendly error message

## Acceptance Criteria

- [ ] Audio is generated in the correct target language matching the word's language
- [ ] Each host's assigned voice is used for audio generation
- [ ] Audio caching works correctly across all three languages
- [ ] Audio for Italian words uses Italian voices
- [ ] Audio for Danish words uses Danish voices
- [ ] Audio for English words uses English voices
- [ ] Example sentence audio works for all three languages
- [ ] Existing Italian audio cache continues to work
- [ ] All 12 host voices can generate audio successfully

## Testing Requirements

- Audio generation produces valid MP3 for an Italian word with an Italian host voice
- Audio generation produces valid MP3 for a Danish word with a Danish host voice
- Audio generation produces valid MP3 for an English word with an English host voice
- Audio caching stores and retrieves files correctly per host
- Audio endpoint returns 401 for unauthenticated requests
- Audio endpoint returns appropriate error for invalid word IDs
