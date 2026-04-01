# Task 010: Frontend Audio Playback

**Feature:** F-AUDIO (Audio Pronunciation), F-EXAMPLE (Example Sentences)
**Priority:** P0
**Dependencies:** 002 (Frontend Scaffolding), 006 (Backend Audio API)
**ADRs:** ADR-0007 (Audio Delivery)

## Description

Implement the AudioButton component that handles word pronunciation playback with sequential example sentence playback. The component must manage a single audio instance globally, support the token-in-query-parameter authentication pattern, and chain word → pause → example sentence playback.

## Technical Requirements

### AudioButton Component

- Renders a speaker icon button (Lucide `Volume2`)
- On click: plays the word pronunciation audio, then automatically plays the example sentence audio after a brief pause
- Audio URL pattern: `/api/audio/{wordId}?token={jwt}` for word, `/api/audio/{wordId}/example?token={jwt}` for example
- Uses the `Audio()` constructor (not `<audio>` DOM elements) for programmatic control

### Playback Behaviour

- **Single instance**: only one audio can play at a time. A module-level variable tracks the current audio instance and word ID.
- **Sequential chaining**: after word audio `onended`, wait ~600ms, then play example audio (if `hasExample` prop is true)
- **Interruptible**: clicking a different word's button stops any currently playing audio chain
- **Toggle**: clicking the same word's button while it's playing stops playback
- **Visual feedback**: pulsing animation on the button while playing
- **Progress tracking**: after the full playback chain completes, call `POST /api/audio/:wordId/listened` (or equivalent) and invoke the `onListened` callback

### Props

- `wordId: string` — The word's database ID
- `italian: string` — The Italian word (for accessible aria-label)
- `token: string | null` — The JWT for query parameter auth
- `hasExample?: boolean` — Whether to play example audio after the word
- `onListened?: () => void` — Callback after playback completes

## Acceptance Criteria

- [ ] Clicking the play button plays the word's pronunciation audio
- [ ] After the word audio ends, the example sentence audio plays automatically (when hasExample is true)
- [ ] Clicking another word's play button stops the current audio
- [ ] Clicking the same word's play button while playing stops playback
- [ ] A visual indicator shows when audio is currently playing
- [ ] Audio works on mobile browsers (iOS Safari, Android Chrome)
- [ ] Play button has accessible aria-label
- [ ] Progress is tracked after playback completes

## Testing Requirements

- AudioButton renders a play button
- AudioButton creates Audio instance with correct URL including token
- AudioButton calls onListened callback after playback
- Button has accessible aria-label with the Italian word
