# Task 006: Backend Audio Generation & Delivery

**Feature:** F-AUDIO (Audio Pronunciation), F-EXAMPLE (Example Sentences)
**Priority:** P0
**Dependencies:** 001 (Backend Scaffolding), 003 (Content Seeding)
**ADRs:** ADR-0016 (Edge TTS with Per-Host Voices), ADR-0007 (Audio Delivery)

> **Note:** The original task referenced Google Translate TTS (ADR-0005, superseded). The active TTS provider is Microsoft Edge TTS via `edge-tts` Python library (ADR-0016).

## Description

Implement the audio generation service using Microsoft Edge TTS (per ADR-0016) to generate MP3 files for all words and example sentences, and the API endpoints that serve cached audio files to authenticated users. Each host has an assigned neural voice; audio is cached per host+word.

## Technical Requirements

### Audio Generation Service

- Async Python service using the `edge-tts` library (`EdgeTTSProvider`)
- Each host has an assigned `edge-tts` neural voice (e.g., `it-IT-DiegoNeural`, `da-DK-JeppeNeural`, `en-GB-ThomasNeural`)
- For each word+host combination, generates two audio files:
  1. Word pronunciation: `audio-cache/{host_id}_{word}.mp3`
  2. Example sentence: `audio-cache/{host_id}_ex_{word}.mp3`
- Skips files that already exist (idempotent)
- Falls back to a DEFAULT_VOICE if the host's assigned voice is unavailable
- Reports progress and any failures

### Audio Delivery Endpoints

- `GET /api/audio/:wordId` — Serve the word pronunciation MP3. Protected by auth middleware (supports token in query parameter per ADR-0007). Look up word by ID to get Italian text, resolve file path from `audio-cache/`. Return with `Content-Type: audio/mpeg`.
- `GET /api/audio/:wordId/example` — Serve the example sentence MP3. Same auth and delivery mechanism. File key: `ex_{italian}.mp3`.

### Progress Tracking

- `POST /api/audio/:wordId/listened` or triggered after audio playback — Record that the user has listened to this word. Create a UserProgress entry (upsert to avoid duplicates).

## Acceptance Criteria

- [ ] `npm run audio:generate` generates MP3 files for all words in the database
- [ ] Existing audio files are not re-generated (idempotent)
- [ ] Example sentence audio is generated alongside word audio
- [ ] `GET /api/audio/:wordId` returns an MP3 file with correct Content-Type
- [ ] `GET /api/audio/:wordId/example` returns the example sentence MP3
- [ ] Audio endpoints accept JWT via query parameter (`?token=`)
- [ ] Audio endpoints return 401 for unauthenticated requests
- [ ] Audio endpoints return 404 for words with missing audio files
- [ ] Listening progress is recorded in the database

## Testing Requirements

- Audio endpoint returns 200 with `audio/mpeg` content type for a valid word
- Audio endpoint returns 401 without authentication
- Audio endpoint returns 404 for non-existent word
- Example audio endpoint returns the correct file
- Listened endpoint creates a UserProgress record
- Listened endpoint is idempotent (no duplicate records)
