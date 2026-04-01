# ADR-0005: Text-to-Speech Provider — Google Translate Free Endpoint with File Caching

- **Status:** Superseded by [ADR-0016](0016-tts-provider-edge-tts.md)
- **Date:** 2026-03-16
- **Deciders:** Development team
- **Requirements:** REQ-3 (Audio pronunciation), REQ-8 (Example sentences)

## Context and Problem Statement

Every word and example sentence in the dictionary needs an Italian pronunciation audio clip (REQ-3, REQ-8). The audio must sound natural, be available for ~370 audio files at launch (184 words + 184 example sentences), and be served with < 1 second latency. The solution must manage API costs and not depend on runtime availability of external services for playback.

## Decision Drivers

- Natural-sounding Italian pronunciation quality
- Cost: free or minimal for the initial corpus (~370 audio files)
- Operational simplicity: avoid runtime dependency on external TTS for playback
- Latency: cached audio must serve in < 1 second
- Scalability: adding new words should not require manual audio recording
- Reliability: audio playback must not fail due to third-party API outages

## Considered Options

### Option 1: Google Translate free TTS endpoint with offline file caching (Chosen)

Use the public `translate.google.com/translate_tts` endpoint to generate MP3 files during a build/seed step. Cache all generated audio as local MP3 files. Serve audio directly from the filesystem at runtime — no external API calls during user requests.

### Option 2: Google Cloud Text-to-Speech API

Official paid API with high-quality WaveNet and Neural2 voices. Provides fine control over voice parameters (speed, pitch, SSML). Free tier includes 1 million characters/month for standard voices. However, requires Google Cloud credentials, project setup, billing account, and the `@google-cloud/text-to-speech` SDK. For ~370 short phrases, the setup overhead exceeds the benefit.

### Option 3: Amazon Polly

AWS's TTS service with neural voices. Comparable quality to Google Cloud TTS. Requires AWS credentials, IAM setup, and SDK integration. Similar overhead concerns as Option 2 for a small corpus.

### Option 4: Pre-recorded human audio

Hire a native Italian speaker to record all pronunciations. Highest quality and most authentic. However, the cost and logistics of recording ~370+ clips (and re-recording when words are added) make this impractical for v1.

### Option 5: Web Speech API (browser-based)

Use the browser's built-in speech synthesis. Zero infrastructure cost. However, voice quality and availability vary dramatically across browsers and operating systems. Italian voices may not be available on all devices. No consistency guarantee.

## Decision Outcome

**Chosen: Option 1 — Google Translate free TTS endpoint with offline file caching**

### Implementation Details

- **Generation script** (`generate-audio.ts`): iterates through all words and example sentences, calls the Google Translate TTS endpoint, and saves MP3 files to `audio-cache/`
- **Endpoint**: `https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=it&q={text}`
- **Runtime**: the Express audio routes serve files directly from `audio-cache/` — no external API calls during user requests
- **Two audio routes**: `/api/audio/:wordId` (word pronunciation) and `/api/audio/:wordId/example` (example sentence)

### Consequences

**Positive:**
- Zero cost: no API keys, billing accounts, or credentials required
- Zero runtime dependency: all audio is pre-generated and served from local files
- Sub-100ms latency for cached audio delivery (file read + HTTP response)
- Idempotent generation: existing files are skipped, only missing audio is generated
- Audio quality is adequate for pronunciation learning (standard Google TTS voice)

**Negative:**
- The free endpoint is undocumented and could change or be rate-limited without notice — mitigated by caching all audio at build time (runtime doesn't depend on the endpoint)
- Single voice only — cannot vary voice per host persona (all four hosts sound the same) — acceptable for v1
- No SSML support — cannot control emphasis, speed, or pauses within individual words
- MP3 files consume disk space (~10-30 KB per file, ~10 MB total for 370 files)

**Neutral:**
- If the free endpoint becomes unavailable, the generation script can be swapped to use Google Cloud TTS or another provider without changing the runtime audio serving logic
- The `@google-cloud/text-to-speech` dependency remains in package.json as a potential upgrade path but is not used at runtime
