# ADR-0012: Story Narration — Edge TTS Streaming with SSML Rate Control

- **Status:** Proposed
- **Date:** 2026-03-29
- **Deciders:** Development team
- **Requirements:** REQ-14 (Story Reading), REQ-3 (Audio pronunciation)

## Context and Problem Statement

The Story Reading feature requires the host to narrate full stories aloud at five user-selectable speeds with karaoke-style word highlighting. The existing TTS approach (ADR-0005) uses the Google Translate free endpoint to pre-generate short audio clips for individual words and example sentences. This approach does not scale to stories for several reasons:

1. **Length limits** — The Google Translate endpoint is designed for short phrases; long texts may be rejected or split unpredictably.
2. **No speed control** — The endpoint provides no parameter for speech rate adjustment; the FRD requires five distinct speeds.
3. **No word-level timing** — Karaoke-style highlighting requires knowing when each word starts and ends in the audio stream; the Google Translate endpoint returns raw MP3 with no timing metadata.
4. **Pre-generation cost** — Pre-generating 27 stories × 12 hosts × 5 speeds = 1,620 audio files is impractical for file-based caching.

A different TTS strategy is needed specifically for story narration.

## Decision Drivers

- Five speed settings: Very Slow, Slow, Normal, Fast, Very Fast
- Karaoke-style word highlighting synced to narration
- Playback must begin within a reasonable time (< 3 s for story narration vs < 1 s for single words)
- Must work with all 12 host personas (distinct TTS voices per host)
- Speed changes during playback should take effect without restarting from the beginning
- Must not pre-generate thousands of audio files
- The Python `edge-tts` library is already a dependency (ADR-0010)

## Considered Options

### Option 1: Edge TTS with SSML rate control and server-side streaming (Chosen)

Use the Python `edge-tts` library to generate narration on-demand via Microsoft Edge's neural TTS service. Use SSML `<prosody rate="...">` to control speech speed. The Edge TTS library provides word-level timing metadata (word boundary events) during generation, which can be returned alongside the audio to power karaoke highlighting. Audio is streamed from the server as it's generated, enabling playback to start before the full story is synthesised.

### Option 2: Pre-generate all speed variants with Google Translate

Generate audio files for all story+host+speed combinations at seed time using the Google Translate endpoint. This is infeasible: 27 stories × 12 hosts × 5 speeds = 1,620 files, the endpoint has no speed parameter, and no word timing is available.

### Option 3: Client-side Web Speech API

Use the browser's built-in `speechSynthesis` API for narration. Supports rate control via `SpeechSynthesisUtterance.rate`. However, voice availability varies across browsers and platforms (many devices lack quality neural voices for Danish/Italian), making it impossible to guarantee consistent host voice identity.

### Option 4: Google Cloud TTS with SSML

Use the paid Google Cloud TTS API with SSML for rate control and audio mark events for timing. Provides high-quality neural voices. However, it requires a billing account, API credentials, and per-character charges. The Edge TTS service provides comparable quality at zero cost.

### Option 5: Pre-generate one speed, adjust playback rate client-side

Generate narration at normal speed and use the Web Audio API's `playbackRate` property to speed up or slow down. This avoids multiple TTS calls but degrades audio quality at extreme speeds (chipmunk effect at high rates, drawl at low rates) and provides no word-level timing data for karaoke highlighting.

## Decision Outcome

**Chosen: Option 1 — Edge TTS with SSML rate control and server-side streaming**

### Implementation Details

**SSML Speed Mapping:**

| UI Speed | SSML `rate` Value | Description |
|---|---|---|
| Very Slow | `x-slow` (≈ 50% normal) | Deliberate pace for parsing each word |
| Slow | `slow` (≈ 75% normal) | Careful, clear enunciation |
| Normal | `medium` (100%) | Natural conversational speed |
| Fast | `fast` (≈ 125% normal) | Slightly accelerated |
| Very Fast | `x-fast` (≈ 150% normal) | Noticeably accelerated |

**SSML Wrapper Example:**
```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="it-IT">
  <voice name="it-IT-IsabellaNeural">
    <prosody rate="slow">
      Buongiorno! Mi chiamo Marco. Sono in un caffè a Roma.
    </prosody>
  </voice>
</speak>
```

**API Endpoint:**

```
GET /api/stories/{storyId}/audio?speed={speed}&token={jwt}
```

Returns a streaming audio response (chunked transfer encoding) with `Content-Type: audio/mpeg`. The server begins streaming audio as soon as the first chunks are available from Edge TTS, enabling playback to start within 2–3 seconds.

**Word Timing Endpoint:**

```
GET /api/stories/{storyId}/timing?speed={speed}&token={jwt}
```

Returns a JSON array of word boundary events:
```json
[
  { "word": "Buongiorno", "offset": 0.0, "duration": 0.85 },
  { "word": "Mi", "offset": 0.95, "duration": 0.15 },
  { "word": "chiamo", "offset": 1.1, "duration": 0.45 }
]
```

The frontend uses this timing data with `requestAnimationFrame` and the audio element's `currentTime` to highlight the current word during playback.

**Caching Strategy:**

- Story narration audio is cached per `storyId + hostVoice + speed` combination.
- Cache key: `story_{storyId}_{voiceName}_{speed}.mp3`
- First request generates and caches; subsequent requests serve from the file cache.
- Word timing data is cached alongside the audio: `story_{storyId}_{voiceName}_{speed}_timing.json`
- At 27 stories × 12 hosts × 5 speeds, the theoretical maximum is 1,620 files — but in practice, users will only trigger generation for the hosts and speeds they use. Generation is lazy (on-demand), not eager.

**Speed Change During Playback:**

When the user changes speed during narration:
1. The frontend notes the current `currentTime` position in the audio.
2. A new audio stream is requested at the new speed.
3. The server generates (or serves from cache) the new speed variant.
4. The frontend seeks to the equivalent position in the new audio using the timing metadata.
5. This causes a brief pause (1–3 s) while the new stream loads — an accepted trade-off documented clearly in the UI (e.g., a loading spinner on the speed control).

### Voice Assignment

Story narration uses the same host voice assignment as single-word pronunciation. The voice is determined by the user's selected host (e.g., host "Marco" → `it-IT-DiegoNeural`). The SSML `<voice>` tag specifies the exact neural voice.

### Consequences

**Positive:**
- Zero cost: Edge TTS is a free service, same as the existing word pronunciation
- Native SSML support enables precise speed control with five distinct rates
- Word boundary events from `edge-tts` provide accurate timing for karaoke highlighting without external alignment tools
- Streaming response enables playback to start before full generation completes
- Lazy caching means only actually-used combinations consume disk space
- Reuses the same token-authenticated audio delivery pattern from ADR-0007

**Negative:**
- Runtime dependency on the Edge TTS service for first-time narration generation — mitigated by caching (subsequent plays are local)
- Speed changes during playback cause a brief interruption (1–3 s) — acceptable trade-off vs. the complexity of real-time speed adjustment
- Cache can grow large if many host+speed combinations are used — mitigated with an optional cache eviction policy (LRU or TTL) for future consideration
- Edge TTS word boundary events may not align perfectly with visible text words (punctuation, contractions) — the frontend must implement fuzzy matching between timing events and rendered tokens

**Neutral:**
- The existing single-word TTS approach (ADR-0005, Google Translate endpoint) remains unchanged for dictionary word pronunciation — story narration is a separate code path
- If Edge TTS becomes unavailable, the fallback is to disable narration with a clear user message; cached audio continues to work
