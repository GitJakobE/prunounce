# ADR-0016: Text-to-Speech Provider — Microsoft Edge TTS with Per-Host Voice Caching

- **Status:** Accepted
- **Date:** 2026-03-29
- **Deciders:** Development team
- **Partially superseded by:** [ADR-0024 (Seeded Audio Generation Strategy)](0024-seeded-audio-generation-strategy.md) for curated audio generation timing
- **Supersedes:** [ADR-0005 (Google Translate Free Endpoint)](0005-tts-provider.md)
- **Requirements:** REQ-3 (Audio pronunciation), REQ-7 (Host personas), REQ-10 (Example sentences)

## Context and Problem Statement

ADR-0005 chose the Google Translate free TTS endpoint for audio generation. That decision assumed a single Italian language with a single voice. The PRD (REQ-3, REQ-7) now requires **multi-language audio** (Italian, Danish, English) with **distinct neural voices per host persona** (12 hosts × 4 per language). The Google Translate endpoint offers no voice selection, no multi-language neural voices, and no async generation support. A new TTS provider is needed that supports per-host voice assignment, all three target languages, and integrates well with the async Python backend (ADR-0010).

## Decision Drivers

- Per-host distinct neural voices (12 hosts, each with a named voice) per F-AUDIO §3.1
- Three target languages: Italian (it-IT), Danish (da-DK), English (en-GB/en-US/en-AU)
- On-demand generation for user-contributed words (REQ-9) — must work at runtime, not just build-time
- Async-native library to match FastAPI's async architecture (ADR-0010)
- Zero API key requirement — no billing accounts or credential management for v1
- Sub-1-second perceived latency for cached audio (F-AUDIO §3.3)
- Audio cached per host+word combination (`word_hostId.mp3`) to avoid regeneration

## Considered Options

### Option 1: Microsoft Edge TTS (`edge-tts` Python library) — Chosen

Use the `edge-tts` library which wraps Microsoft's Edge browser speech synthesis service. Provides access to 400+ neural voices across all target languages with native `async`/`await` support. No API key required. Voices are specified by name (e.g., `it-IT-DiegoNeural`, `da-DK-JeppeNeural`).

### Option 2: Google Translate free endpoint (Status quo — ADR-0005)

The existing approach. Single voice per language, no voice selection, no async support, no SSML. Cannot support per-host voice differentiation.

### Option 3: Google Cloud Text-to-Speech API

Official paid API with WaveNet/Neural2 voices. Excellent quality and voice selection. Requires Google Cloud credentials, billing account, and SDK setup. The operational overhead and cost are disproportionate for an application that can use free neural voices of comparable quality.

### Option 4: Azure Cognitive Services Speech

Microsoft's paid speech service with extensive voice catalogue. Excellent quality but requires Azure subscription and Speech resource provisioning. Would align with the Azure deployment target but adds cost and credential management complexity for v1.

### Option 5: gTTS (Google Translate TTS Python wrapper)

Python wrapper around the free Google Translate endpoint. Simpler than raw HTTP calls. Same limitations as Option 2 — single voice per language, no voice selection, synchronous only.

## Decision Outcome

**Chosen: Option 1 — Microsoft Edge TTS (`edge-tts`)**

### Implementation Details

- **Library:** `edge-tts` (Python, async-native)
- **Fallback:** `gTTS` retained as a secondary dependency for resilience (not currently used in primary path)
- **Provider abstraction:** `TTSProvider` ABC in `app/services/tts.py` with `EdgeTTSProvider` as the default implementation — allows swapping to a different provider without changing callers
- **Voice assignment:** Each host persona declares a `voice.voiceName` field (e.g., `it-IT-DiegoNeural`). The audio router resolves the user's current host and passes the voice name to the TTS provider.
- **Cache key:** `{sanitized_word}_{hostId}.mp3` — audio is cached per host voice so different hosts produce different pronunciations
- **Speed control:** Single-word pronunciations use `rate=-30%` for learner clarity; example sentences play at normal speed
- **Cache directory:** Configurable via `AUDIO_CACHE_DIR` setting (default: `audio-cache/`)
- **On-demand generation:** When a cached file doesn't exist, it is generated synchronously on first request and cached for all subsequent plays (F-AUDIO §3.5)

### Voice Assignments

| Host | Language | Voice |
|---|---|---|
| Marco | it-IT | `it-IT-DiegoNeural` |
| Giulia | it-IT | `it-IT-IsabellaNeural` |
| Luca | it-IT | `it-IT-GiuseppeMultilingualNeural` |
| Sofia | it-IT | `it-IT-ElsaNeural` |
| Anders | da-DK | `da-DK-JeppeNeural` |
| Freja | da-DK | `da-DK-ChristelNeural` |
| Mikkel | da-DK | `da-DK-JeppeNeural` (alternate pitch planned) |
| Ingrid | da-DK | `da-DK-ChristelNeural` (alternate pitch planned) |
| James | en-GB | `en-GB-RyanNeural` |
| Emma | en-GB | `en-GB-SoniaNeural` |
| Ryan | en-AU | `en-AU-WilliamNeural` |
| Margaret | en-GB | `en-GB-LibbyNeural` |

### Consequences

**Positive:**
- Zero cost and zero API keys — same operational simplicity as ADR-0005
- 400+ neural voices available — each host gets a distinct, named voice
- Native async support integrates cleanly with FastAPI's async handlers
- Provider abstraction (`TTSProvider` ABC) makes future migration to a paid service straightforward
- Per-host caching ensures users hear their host's voice, not a generic voice

**Negative:**
- `edge-tts` depends on Microsoft's Edge speech service availability — mitigated by caching all generated audio
- Danish has only 2 neural voices (`da-DK-JeppeNeural`, `da-DK-ChristelNeural`) for 4 Danish hosts — resolved with pitch/rate variation or future voice additions
- Runtime TTS generation for uncached words adds latency on first play (~1-3 seconds) — acceptable per F-AUDIO §3.2 edge case guidance
- `asyncio.run()` is called inside a sync FastAPI endpoint — blocking but functional; future improvement to convert audio endpoints to `async def`

**Neutral:**
- `gTTS` remains as a dependency but is not invoked in the current primary path; its role is as a documented fallback
- ADR-0007 (Audio Delivery — file caching + HTTP serving) remains valid and complementary
