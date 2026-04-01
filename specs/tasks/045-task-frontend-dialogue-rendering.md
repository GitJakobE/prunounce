# Task 045: Frontend Dialogue Story Rendering

**Feature:** F-DIALOGUE (Story Dialogue Formatting)
**Priority:** P1
**Dependencies:** 044 (Backend Dialogue API), 033 (Frontend Story Library & Reading View)

## Description

Update the frontend story reading view to render dialogue stories in a play/script format with speaker labels, and narrative stories as flowing paragraphs. The reading view must detect the story format from the API response and render accordingly. Word click and translation panel functionality must work identically in both formats.

## Technical Requirements

### Story Format Detection

- Read the `format` field from the story detail API response
- Read the `segments` array for the parsed body structure
- If `format` is `"narrative"`: render using existing paragraph-based layout
- If `format` is `"dialogue"` or `"mixed"`: render using the segment-based layout described below

### Dialogue Rendering

- Each dialogue segment renders as a distinct visual block:
  - **Speaker label** displayed in bold, followed by a colon separator
  - **Spoken text** displayed after the separator as regular-weight text
  - Each turn occupies its own line/block with vertical spacing between turns
- Speaker labels must be styled distinctly from spoken text (bold weight, optionally a different colour)
- **Speaker colour coding**: assign a consistent accent colour to each speaker (2–4 colours from the palette). Colours must meet WCAG AA contrast requirements and not rely on colour alone (the speaker name is also present).
- Narration segments within a mixed story render as standard paragraphs, visually distinct from dialogue (e.g., italic text, reduced opacity, or indentation)

### Word Tokenisation for Dialogue

- Tokenise only the **spoken text** portion of each dialogue segment (not the speaker label)
- Speaker labels are rendered as plain, non-clickable text
- Word click, highlighting, and translation panel behaviour are identical to narrative stories
- Punctuation handling rules are unchanged

### Responsive Layout

- On mobile: speaker label and text stack naturally; label above text if needed to avoid overflow
- On tablet/desktop: speaker label and text on the same line (label as a fixed-width column, text flowing)
- Long speaker labels truncate with ellipsis on very small viewports

### Story Library Page

- Add a small visual indicator on story cards to show whether a story is dialogue format (e.g., a speech-bubble icon or "Dialogue" chip)
- This uses the `format` field from the story list API response

### i18n

- No new translatable strings required (speaker labels come from story content, not UI)
- Ensure any accessibility labels (ARIA) for dialogue structure are translatable if added

### Accessibility

- Use semantic HTML for dialogue rendering: `<dl>` (definition list) with `<dt>` for speaker and `<dd>` for text, or equivalent structure that conveys speaker attribution to screen readers
- Each dialogue turn should be announced with the speaker name followed by their text
- Keyboard navigation: Tab through dialogue turns should follow reading order

## Acceptance Criteria

- [ ] Dialogue stories render in play/script format with speaker labels
- [ ] Each speaker turn is on its own line/block
- [ ] Speaker labels are bold and visually distinct from spoken text
- [ ] Speaker colour coding applied (accessible, meets WCAG AA)
- [ ] Narrative stories continue to render as paragraphs unchanged
- [ ] Mixed stories render both narrative and dialogue sections appropriately
- [ ] Speaker labels are not clickable for dictionary lookup
- [ ] Word click and translation panel work identically in dialogue stories
- [ ] Story cards show dialogue format indicator
- [ ] Layout is responsive across mobile, tablet, and desktop
- [ ] Screen readers announce speaker names with their text

## Testing Requirements

- Dialogue story renders correct number of speaker turns
- Each turn displays the correct speaker label and text
- Speaker labels are not clickable (click events are not triggered)
- Words in dialogue text are clickable and trigger translation lookup
- Narrative story renders as paragraphs (regression test)
- Mixed story renders both formats correctly
- Colour assignments are consistent for the same speaker throughout the story
- Responsive layout verified at mobile, tablet, and desktop breakpoints
