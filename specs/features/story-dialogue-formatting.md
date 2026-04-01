# Feature Requirements Document — Story Dialogue Formatting

**Parent PRD:** [prd.md](../prd.md)
**Feature ID:** F-DIALOGUE
**Priority:** P1 (Enhancement to F-STORY)
**Related:** [story-reading.md](story-reading.md), REQ-14

---

## 1. Overview

Many of the curated stories in Pronuncia are conversations between two people — ordering at a café, shopping at a market, visiting a doctor, introducing yourself to a neighbour. Currently, these conversations are stored and displayed as flat, continuous text with no indication of who is speaking. This makes it difficult for learners to follow the dialogue flow, understand turn-taking, and connect phrases to the correct speaker.

This feature introduces **dialogue formatting** for conversational stories, presenting them in a play/script style with clear speaker labels so users always know who is saying what. Stories that are pure narration (e.g., folk tales, descriptive passages) remain unaffected.

## 2. Problem Statement

- Conversational stories are rendered as a wall of text with no visual distinction between speakers.
- Learners cannot tell who is saying which line, making it harder to understand conversational patterns and turn-taking.
- During host narration (read-aloud), there is no way to distinguish between the voices of different characters in a dialogue.
- The flat text format does not reflect how real conversations work, reducing the immersion and educational value of the content.

## 3. User Stories

| ID | Story | Acceptance Criteria |
|---|---|---|
| US-D1 | As a learner, I want to see who is speaking each line of a dialogue story, so that I can follow the conversation naturally. | Each line of dialogue is prefixed with a speaker label (e.g., character name or role). |
| US-D2 | As a learner, I want dialogue stories to look like a script or play, so that I can easily distinguish between speakers. | Dialogue lines are visually separated, with speaker names styled distinctly from spoken text. |
| US-D3 | As a learner, I want narrative (non-dialogue) stories to remain in paragraph form, so that both formats are presented appropriately. | Stories without speaker labels render as flowing paragraphs, unchanged from the current behaviour. |
| US-D4 | As a learner, I want to hear different vocal characteristics when the host narrates a dialogue, so that I can distinguish between characters by ear. | During narration, distinct characters in a dialogue are voiced with recognisable variation (e.g., different pitch, pacing, or a second TTS voice). |
| US-D5 | As a learner, I want to click any word in a dialogue line and look it up, so that the translation panel works the same as in non-dialogue stories. | Word-click and translation panel functionality is unaffected by dialogue formatting. |

## 4. Functional Requirements

### 4.1 Story Content Types

The system must support two story content types:

- **Narrative** — Continuous prose text (no speaker attribution). Displayed as paragraphs. This is the existing default.
- **Dialogue** — A sequence of attributed lines, each associated with a named speaker. Displayed in play/script format.

A single story may contain **both** narrative sections and dialogue sections (e.g., a brief scene-setting paragraph followed by a conversation).

### 4.2 Dialogue Content Structure

- Each dialogue line must be associated with a **speaker label** — a character name or role (e.g., "Marco", "Sofia", "Cameriere", "Cliente").
- Speaker labels must be in the **target language** of the story (i.e., Italian character names for Italian stories).
- Speaker labels must be short and consistent within a story (same character always uses the same label).
- Each story should have **no more than 4 named speakers** to keep dialogues manageable for learners.
- A story's metadata must indicate whether it contains dialogue, so the frontend can choose the appropriate rendering.

### 4.3 Dialogue Display

- Dialogue lines must be displayed in a **script/play format**:
  - Each line starts with the **speaker label** in bold or a visually distinct style, followed by a separator (e.g., colon or em-dash), then the spoken text.
  - Each speaker turn occupies its own visual line or block — dialogue is **not** run together as a paragraph.
  - Consecutive lines from the same speaker may be grouped if they represent a single uninterrupted turn.
- **Speaker colour coding** (optional enhancement): Each speaker may be assigned a distinct accent colour to further differentiate turns visually. Colours should be accessible (sufficient contrast, not colour-only differentiation).
- Narrative sections within a mixed story must be visually distinct from dialogue (e.g., no speaker label, different indentation or font style).
- The layout must remain responsive: on mobile, speaker labels and text must not overflow or become unreadable.

### 4.4 Narration of Dialogue Stories

- When the host narrates a dialogue story, the system should provide **vocal differentiation** between speakers so the listener can distinguish who is talking.
- Acceptable approaches for vocal differentiation (implementation choice left to development team):
  - Using a distinct TTS voice for each character
  - Varying pitch or speaking rate per character
  - Using a brief pause or audio cue between speaker turns
- At minimum, there must be a **clear pause between speaker turns** during narration so the listener can recognise when the speaker changes.
- Karaoke-style text highlighting during narration must highlight the **current speaker's label and their line** together so the user can see both who is speaking and what they are saying.

### 4.5 Word Interaction in Dialogue

- Every word in dialogue text must remain individually clickable, exactly as in narrative stories.
- Speaker labels are **not** clickable for dictionary lookup (they are character names, not vocabulary).
- Punctuation handling, dictionary lookup fallback behaviour, and translation panel behaviour must be identical to narrative stories.

### 4.6 Backward Compatibility

- Existing stories that are currently stored as flat text must continue to render correctly as narrative stories without any changes to their data.
- The dialogue format is additive — it applies only to stories whose content is structured with speaker labels.
- The Story API response must include enough information for the frontend to determine whether a story is narrative, dialogue, or mixed.

## 5. Content Guidelines for Dialogue Stories

- Each dialogue story should involve a realistic, everyday scenario between 2–3 characters.
- Characters should have culturally appropriate names for the target language.
- Speaker labels should be the character's first name or a role descriptor (e.g., "Dottoressa", "Venditore") — whichever is clearest for the learner.
- Stage directions or scene-setting narration (e.g., "Marco walks into the café.") may appear as narrative text between dialogue lines.
- All existing conversational stories (café, market, doctor, restaurant, neighbour introduction, etc.) should be reformatted into dialogue format as part of this feature.

## 6. Edge Cases

- A story with only one speaker (e.g., a monologue or speech) should be treated as narrative, not dialogue.
- If a speaker label is very long (e.g., "Il proprietario del ristorante"), it should truncate or wrap gracefully on small screens.
- If the TTS service cannot provide a second voice for dialogue narration, the system should fall back to single-voice narration with clear pauses between turns.
- Quoted speech within narrative text (e.g., a folk tale where a character speaks) is not the same as dialogue format — it remains as narrative text unless explicitly structured with speaker labels.

## 7. Acceptance Criteria

- [ ] The data model or content format supports dialogue-attributed lines with speaker labels.
- [ ] Stories with dialogue are rendered in a play/script format with speaker names visually distinct from spoken text.
- [ ] Each speaker turn is displayed on its own line or block.
- [ ] Narrative stories continue to render as paragraphs, unchanged.
- [ ] Mixed stories (narrative + dialogue) render both sections appropriately.
- [ ] All existing conversational stories are reformatted to include speaker labels.
- [ ] Word click and translation panel functionality works identically in dialogue stories.
- [ ] Speaker labels are not clickable for dictionary lookup.
- [ ] Host narration of dialogue stories includes clear pauses between speaker turns at minimum.
- [ ] Karaoke highlighting in dialogue stories highlights the current speaker label and their line.
- [ ] Dialogue formatting renders correctly on mobile, tablet, and desktop.
- [ ] The Story API response indicates whether a story contains dialogue.
