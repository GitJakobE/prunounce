# Task 036: Story Accessibility & Responsive Audit

**Feature:** Cross-cutting (F-A11Y, F-RESPONSIVE, F-STORY)
**Priority:** P1
**Dependencies:** 015 (Responsive Design & Accessibility), 033 (Frontend Story Library), 034 (Frontend Narration Player)

## Description

Extend the accessibility and responsive design coverage from task 015 to include all story reading components. This task verifies that the story library, reading view, translation panel, and narration player meet WCAG 2.1 AA compliance and render correctly across all breakpoints. It also ensures the karaoke highlighting is accessible to screen readers and that narration controls are fully keyboard-operable.

## Technical Requirements

### Story Library Accessibility

- Story cards must be keyboard-navigable (Tab to focus, Enter to open)
- Difficulty badges must not convey information by colour alone — include text label
- Reading time must be exposed to screen readers
- Difficulty group headings must use proper heading hierarchy (`h2` or `h3`)

### Reading View Accessibility

- Clickable words must be focusable and activatable via Enter/Space key
- Active/highlighted word must have `aria-current="true"` during karaoke playback
- Translation panel must receive focus when opened and announce content via `aria-live="polite"`
- Translation panel close button must return focus to the previously selected word
- Story body text must have appropriate `lang` attribute matching the target language

### Narration Player Accessibility

- All controls (Play/Pause, Stop, Speed) must have `aria-label` and be keyboard-operable
- Current playback state must be announced via `aria-live` region (e.g., "Playing", "Paused", "Stopped")
- Speed selector must announce the selected speed
- Space bar toggles play/pause when player has focus (already specified in task 034)

### Responsive Layout Verification

- Story library grid: 1 column at 375px, 2 columns at 768px, 3 columns at 1280px
- Reading view: body text max-width ~65ch, comfortable line-height (1.6–1.8)
- Translation panel: full-width bottom overlay on mobile, inline bottom bar on desktop
- Narration player: compact bar that does not obscure story text
- No horizontal scrolling on any story page at any breakpoint
- Touch targets: all interactive elements meet 44×44px minimum

### Screen Reader Testing

- VoiceOver (macOS/iOS) and NVDA (Windows) must be able to:
  - Navigate story library cards
  - Read story body text
  - Activate word translation by pressing Enter on a focused word
  - Hear translation panel content
  - Control narration playback

## Acceptance Criteria

- [ ] Story cards are keyboard-navigable and announce title, difficulty, and reading time
- [ ] Difficulty badges include text labels (not colour only)
- [ ] Clickable words are focusable and activatable via keyboard
- [ ] Karaoke-highlighted word has `aria-current="true"`
- [ ] Translation panel is announced via `aria-live` and manages focus correctly
- [ ] Narration controls have ARIA labels and keyboard support
- [ ] Story body has correct `lang` attribute
- [ ] Story pages have no horizontal scroll at 375px, 768px, and 1280px
- [ ] All touch targets meet 44×44px minimum
- [ ] Colour contrast meets WCAG AA on all story components

## Testing Requirements

- Automated a11y audit (axe-core or Lighthouse) on story library and reading view pages
- Keyboard-only navigation test: complete the full story flow without a mouse
- Screen reader announcement verification for translation panel and narration state
- Responsive snapshot tests at 375px, 768px, and 1280px for story library and reading view
- Colour contrast check on difficulty badges, translation panel, and karaoke highlighting
