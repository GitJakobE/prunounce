# Task 034: Frontend Story Narration Player

**Feature:** F-STORY (Story Reading)
**Priority:** P1
**Dependencies:** 033 (Frontend Story Library & Reading View), 031 (Story Narration TTS Service)

## Description

Build the audio narration player for the story reading view. The player allows users to listen to the story narrated by their selected host persona's voice with five speed options. During narration, words are highlighted in sync with the audio using word boundary timing data from the backend (karaoke-style highlighting). The player includes play/pause/stop controls and a speed selector.

## Technical Requirements

### Narration Player Component

- Render a persistent player bar at the top or bottom of the story reading view
- Controls:
  - **Play/Pause** toggle button
  - **Stop** button (resets to beginning)
  - **Speed selector** — dropdown or segmented control with options: 0.5×, 0.75×, 1×, 1.25×, 1.5×
- Player state management:
  - `idle` → `loading` → `playing` ↔ `paused` → `idle` (on stop or end)
  - Show loading spinner while audio is buffering

### Audio Streaming

- On play, fetch audio from `GET /api/stories/:storyId/narrate?hostId=X&speed=Y`
- Use the Web Audio API or HTML5 `<audio>` element for streaming playback
- Changing speed during playback: stop current audio, re-fetch with new speed, resume from beginning
- Use the user's currently selected host persona for the `hostId` parameter

### Karaoke Highlighting

- On play (or before), fetch word boundary timing from `GET /api/stories/:storyId/timing?hostId=X&speed=Y`
- During playback, use `requestAnimationFrame` or `setInterval` synchronised with audio `currentTime` to determine which word should be highlighted
- Highlighted word: apply a distinct visual style (e.g., bold + background colour) to the current word in the story body
- As audio progresses, highlighting moves from word to word in sync
- When audio ends or is stopped, remove all word highlighting

### Integration with Reading View

- The narration player must coexist with the translation panel from task 033
- Clicking a word during narration should still trigger the translation panel (both features active simultaneously)
- If narration is playing and a word is clicked, the translation panel opens but narration continues

### Accessibility

- Play/Pause and Stop buttons must have `aria-label` attributes
- Speed selector must be keyboard-navigable
- Current narration state must be announced via `aria-live` region
- Keyboard shortcut: Space to toggle play/pause when player is focused

## Acceptance Criteria

- [ ] Narration player renders with Play/Pause, Stop, and Speed controls
- [ ] Pressing Play fetches and streams audio from the narration endpoint
- [ ] Audio uses the user's selected host persona's voice
- [ ] All five speed options produce correctly paced narration
- [ ] Karaoke highlighting tracks the current word during playback
- [ ] Highlighting is visually distinct and moves in sync with audio
- [ ] Stop resets playback and removes highlighting
- [ ] Pause halts audio and highlighting; resume continues
- [ ] Changing speed re-fetches audio at the new speed
- [ ] Translation panel still works during active narration
- [ ] Player controls have appropriate ARIA labels
- [ ] Loading state is shown while audio buffers

## Testing Requirements

- Player renders all controls (play/pause, stop, speed selector)
- Play button triggers narration API call with correct hostId and speed
- Speed selector sends correct speed parameter to API
- Stop resets player state to idle
- Pause and resume toggle correctly
- Word highlighting activates during playback (mock timing data)
- Word highlighting deactivates on stop
- Translation panel opens on word click during narration
- ARIA labels are present on all interactive elements
- Loading spinner shows during audio fetch
