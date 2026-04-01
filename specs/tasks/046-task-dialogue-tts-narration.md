# Task 046: Dialogue-Aware TTS Narration

**Feature:** F-DIALOGUE (Story Dialogue Formatting)
**Priority:** P2
**Dependencies:** 042 (Story Dialogue Body Format), 044 (Backend Dialogue API), 031 (Story Narration TTS)

## Description

Update the story narration TTS pipeline to produce more natural-sounding audio for dialogue stories. At minimum, insert clear pauses between speaker turns. Optionally, use distinct TTS voice characteristics per speaker for richer differentiation. Update the frontend narration player to highlight dialogue turns during karaoke-style playback.

## Technical Requirements

### Backend TTS Changes

#### Pause Insertion Between Turns

- When generating narration audio for a dialogue-format story, insert an SSML `<break>` element between speaker turns
- Recommended pause duration: 400–600ms between turns (enough to signal a speaker change without disrupting flow)
- Use SSML structure:
  ```xml
  <speak>
    <voice name="...">
      <prosody rate="...">
        Buongiorno! Vorrei un caffè, per favore.
        <break time="500ms"/>
        Certo, subito. Vuole anche qualcosa da mangiare?
        <break time="500ms"/>
        Sì, un cornetto, grazie.
      </prosody>
    </voice>
  </speak>
  ```
- For narrative segments in mixed stories, no extra breaks are inserted (natural paragraph flow)

#### Optional Voice Variation (Enhancement)

- If the Edge TTS voice supports pitch/rate variation via SSML `<prosody>`, assign slightly different pitch offsets to different speakers
- Example: Speaker A at `pitch="+0Hz"`, Speaker B at `pitch="+20Hz"` (subtle differentiation)
- If the TTS provider does not support fine-grained pitch control, fall back to the pause-only approach
- Do not attempt to use a completely different TTS voice per speaker — this would require multiple voice assignments per host and is out of scope

#### Audio Cache Invalidation

- Dialogue-format narration audio should be cached with a different cache key than the original flat-text narration
- Cache key pattern: `story_{story_id}_{host_id}_{safe_rate}_v2.mp3`
- Old cache files for reformatted stories should be cleared during deployment or the first regeneration

### Frontend Karaoke Highlighting for Dialogue

- During narration playback, the karaoke highlight must track which dialogue turn is currently being spoken
- The highlight should encompass both the **speaker label** and the **spoken text** of the current turn
- Turns before the current position should show a "read" state (dimmed or faded)
- Turns after the current position remain in default state
- When narration enters a narrative segment (in mixed stories), highlighting reverts to word/sentence-level tracking

### Word Timing for Dialogue

- If Edge TTS provides word-boundary events during generation, these should be captured and returned to the frontend for precise word-level highlighting
- If word-boundary events are not available, fall back to estimated timing based on word count per turn and total audio duration
- Timing data format in the API response (new optional field on the narration audio endpoint or a separate endpoint):
  ```json
  {
    "timing": [
      {"segment_index": 0, "start_ms": 0, "end_ms": 2500},
      {"segment_index": 1, "start_ms": 3000, "end_ms": 5200},
      ...
    ]
  }
  ```

## Acceptance Criteria

- [ ] Dialogue story narration includes audible pauses (400–600ms) between speaker turns
- [ ] Narrative stories and narrative segments in mixed stories are narrated without extra pauses (unchanged behaviour)
- [ ] Audio cache key differentiates dialogue-format narration from legacy flat-text cache
- [ ] Karaoke highlighting tracks the current dialogue turn (speaker label + text)
- [ ] Turns before/after the current turn are visually distinguished
- [ ] Narration works at all five speed settings with dialogue pauses
- [ ] TTS generation handles both dialogue and narrative body formats without errors
- [ ] Fallback to single-voice narration with pauses if pitch variation is unsupported

## Testing Requirements

- Dialogue story narration audio is generated successfully at all five speeds
- Generated audio includes detectable silence gaps between turns (verify file duration is longer than equivalent flat-text narration)
- Narrative story narration is unchanged (regression)
- Cache key includes version suffix for dialogue-format stories
- Frontend karaoke highlighting moves through dialogue turns in order
- Highlighting correctly covers speaker label + text together
- Speed changes mid-playback work correctly with dialogue narration
