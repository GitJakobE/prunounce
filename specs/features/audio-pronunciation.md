# Feature Requirements Document — Audio Pronunciation

**Parent PRD:** [prd.md](../prd.md)
**Feature ID:** F-AUDIO
**Priority:** P0 (Must-have for launch)

## 1. Overview

Every word in the dictionary has an associated pronunciation audio clip in its target language. Audio is generated using Microsoft Edge TTS neural voices, with each host persona having a distinct voice. Users trigger playback by clicking or tapping a word or its play button. Playback must feel instant and be replayable without limit.

## 2. User Stories

| ID | Story | Acceptance Criteria |
|---|---|---|
| US-A1 | As a learner, I want to click a word and immediately hear it pronounced in the target language. | Clicking a word or its play button starts audio playback within 1 second. |
| US-A2 | As a learner, I want to replay a pronunciation as many times as I need. | No limit on replays; each click restarts the audio from the beginning. |
| US-A3 | As a mobile user, I want audio to work on my phone without extra plugins. | Audio plays natively on iOS Safari, Android Chrome, and major desktop browsers. |
| US-A4 | As a learner browsing a word list, I want to stop one word's audio when I play another. | Playing a new word automatically stops any currently playing audio. |
| US-A5 | As a user with a specific host, I want to hear words in my host's voice. | Audio is generated and cached per host voice, and plays using the selected host's TTS voice. |

## 3. Functional Requirements

### 3.1 Audio Source
- All pronunciation audio must be generated using Microsoft Edge TTS (msedge-tts) neural voices.
- Each host persona has a dedicated TTS voice in their native language:
  - **Italian hosts:** 4 distinct Italian (it-IT) neural voices
  - **Danish hosts:** 4 distinct Danish (da-DK) neural voices
  - **English hosts:** 4 distinct English neural voices (mix of en-GB, en-US, en-AU as appropriate to persona)
- Audio must be generated for every word in the dictionary in the appropriate target language.

### 3.2 Playback Trigger
- Each word entry must have an easily identifiable play button (speaker icon or similar).
- Clicking/tapping either the word text itself or the play button must trigger playback.
- On touch devices, the tap target must be at least 44 × 44 px for accessibility.

### 3.3 Playback Behaviour
- Audio must begin within 1 second of the user interaction.
- If another word's audio is already playing, it must stop before the new word's audio begins.
- Users may replay the same word's audio unlimited times.
- A visual indicator (e.g., animated speaker icon) should show when audio is currently playing.

### 3.4 Audio Delivery & Caching
- Once an audio clip has been generated for a word+host combination, it must be stored/cached so that subsequent plays do not call the TTS service again.
- Audio files are cached per host voice (e.g., `bruschetta_marco.mp3`, `bruschetta_giulia.mp3`).
- Repeated playback of the same word by any user with the same host must not incur additional TTS generation.
- Regardless of delivery strategy, the perceived latency for the user must not exceed 1 second.

### 3.5 Multi-Language Audio
- The TTS voice language must match the target language of the word.
- Italian words are spoken by Italian voices, Danish words by Danish voices, English words by English voices.
- User-contributed words trigger automatic audio generation in the target language using the contributor's current host voice. Audio for other hosts' voices is generated on-demand when another user with a different host plays the word.

### 3.6 Accessibility
- Play buttons must have appropriate labels for screen readers (e.g., "Play pronunciation of [word]").
- Audio must not autoplay on page load.

## 4. Edge Cases

- If the TTS service is temporarily unavailable, display a user-friendly error message: "Pronunciation temporarily unavailable. Please try again shortly."
- For user-contributed words, if audio hasn't been generated yet, show a brief loading indicator then generate on-demand.
- For words with multiple valid pronunciations, use the most common standard pronunciation.

## 5. Acceptance Criteria

- [ ] Every word in the dictionary has playable pronunciation audio in the correct target language.
- [ ] Audio is generated via Microsoft Edge TTS with distinct neural voices per host.
- [ ] Playback starts within 1 second of user interaction.
- [ ] Playing a new word stops any currently playing audio.
- [ ] Audio works on mobile browsers (iOS Safari, Android Chrome) without plugins.
- [ ] Play buttons are accessible to screen readers.
- [ ] A clear error message is shown when audio is unavailable.
- [ ] Audio is cached per host+word — replaying does not trigger new TTS generation.
- [ ] User-contributed words get audio generated automatically.
