# Task 059: Pronounce Audio Endpoint

**Feature:** F-OTFLOOKUP (On-the-Fly Word Lookup & Audio)
**Priority:** P1
**Dependencies:** 057 (Translation Service — shares TTS infrastructure)

## Description

Add a new `GET /api/audio/pronounce` endpoint that generates pronunciation audio for arbitrary text (words not in the curated `Word` table). This endpoint reuses the existing `get_audio_path()` generate-on-miss mechanism and `EdgeTTSProvider` but accepts raw text + language instead of a `word_id`. A per-user in-memory rate limiter protects against abuse.

## Technical Requirements

### New Endpoint

- **Route:** `GET /api/audio/pronounce`
- **Query Parameters:**
  - `word` (required, string) — the text to pronounce
  - `lang` (required, string) — ISO 639-1 language code (`it`, `en`, `da`)
- **Auth:** `get_current_user_id` dependency (JWT via `?token=` query param, matching existing audio endpoints)
- **Response:** `FileResponse` with `audio/mpeg` and Cache-Control `public, max-age=31536000, immutable`

### Route Ordering

- The `/pronounce` route MUST be registered **before** the `/{word_id}` route in the audio router to prevent FastAPI from matching "pronounce" as a `word_id` path parameter
- Move or reorder route definitions in `app/routers/audio.py` accordingly

### Input Validation

- Maximum length: 100 characters
- Allowed characters: Unicode letters, spaces, apostrophes, hyphens (regex: `^[\p{L}\s'\-]{1,100}$` using the `regex` module or equivalent)
- `lang` must be one of `it`, `en`, `da`
- Return 400 (Bad Request) for invalid input with a descriptive error message

### Voice Selection

- Reuse `resolve_host_voice(user_id, db)` to get the user's preferred host voice
- Validate that the host's language matches the requested `lang` parameter
- If the host language doesn't match, select a default voice for the requested language (e.g., look up a host that speaks the requested language)

### Audio Generation

- Use `get_audio_path(word, None, host_id, voice_name)` — same pattern as `word_audio()`
- The `filename_key` is the raw word text (sanitized via `sanitize_filename()` inside `get_audio_path`)
- Audio is cached on disk automatically by the existing mechanism

### Per-User Rate Limiter

- Create a new generic rate limiter (e.g., `app/rate_limit.py: check_user_rate()`) distinct from the existing login rate limiter
- In-memory sliding window: **60 requests per minute per user**
- Key: user ID (not email)
- Return 429 (Too Many Requests) when exceeded
- The existing `check_login_allowed()` is login-specific and must not be modified

### Error Handling

- TTS generation failure → 503 with "Pronunciation temporarily unavailable"
- Invalid input → 400 with descriptive message
- Rate limit exceeded → 429
- Unauthenticated → 401 (handled by dependency)

## Acceptance Criteria

- [ ] `GET /api/audio/pronounce?word=ciao&lang=it` returns MP3 audio
- [ ] Route is matched before `/{word_id}` (no path conflict)
- [ ] Input validation rejects words > 100 chars, invalid characters, and unsupported languages
- [ ] Per-user rate limiter enforces 60 req/min ceiling
- [ ] Audio is cached on disk — second request for same word/host returns cached file
- [ ] Voice is selected based on user's host preference (or default for requested language)
- [ ] 503 returned when TTS generation fails
- [ ] 400 returned for invalid input
- [ ] 429 returned when rate limit exceeded
- [ ] Existing `/{word_id}` and `/{word_id}/example` endpoints remain unaffected

## Testing Requirements

- Valid request returns audio/mpeg file response
- Route ordering: `GET /api/audio/pronounce` matches before `/{word_id}`
- Input validation rejects empty string, oversized input, special characters, unsupported lang codes
- Rate limiter allows up to 60 requests per minute and blocks the 61st
- Rate limiter uses user_id key (different users have independent limits)
- Cached audio file is reused on subsequent requests (verify `get_audio_path` returns existing path)
- TTS failure returns 503
- Unauthenticated request returns 401
