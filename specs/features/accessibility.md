# Feature Requirements Document — Accessibility & Inclusive Design

**Parent PRD:** [prd.md](../prd.md)
**Feature ID:** F-A11Y
**Priority:** P0 (Must-have for launch)
**Review Panel Persona:** Farah (Inclusive Tester)

---

## 1. Overview

Pronuncia must be usable by people with a wide range of abilities, including users who rely on screen readers, keyboard-only navigation, or high-contrast display modes. The product targets WCAG 2.1 Level AA conformance across all pages and interactive flows. Accessibility is a cross-cutting concern that applies to every feature; this FRD defines the holistic standards and acceptance criteria that every page, component, and interaction must meet.

## 2. User Stories

| ID | Story | Acceptance Criteria |
|---|---|---|
| US-A1 | As a screen-reader user, I want every interactive element to have a meaningful accessible name, so that I can understand what each control does without seeing the screen. | All buttons, links, inputs, and custom controls have programmatic labels (aria-label, aria-labelledby, or visible label association). No unlabelled interactive elements exist. |
| US-A2 | As a keyboard-only user, I want to navigate every feature without a mouse, so that I can use the app with a keyboard or switch device. | All interactive elements are reachable via Tab / Shift+Tab. Focus order follows a logical reading sequence. No keyboard traps exist. |
| US-A3 | As a user with low vision, I want sufficient colour contrast on all text and interactive elements, so that I can read content without straining. | All text meets WCAG AA contrast ratios (4.5:1 for normal text, 3:1 for large text). UI components and graphical objects meet 3:1 against adjacent colours. |
| US-A4 | As a screen-reader user, I want dynamic content changes (search results, language switch, progress updates) announced automatically, so that I'm aware of what changed without re-scanning the page. | Dynamic regions use ARIA live regions (aria-live="polite" or "assertive" as appropriate). Toast messages, error alerts, and inline result updates are announced. |
| US-A5 | As a user who magnifies my screen to 200%, I want the layout to reflow without horizontal scrolling, so that I can read content at my preferred zoom level. | No horizontal scrollbar appears at 200% zoom on a 1280px-wide viewport. All content remains readable and functional. |
| US-A6 | As a user who is sensitive to motion, I want to disable or reduce animations, so that the interface does not cause discomfort. | The site respects the `prefers-reduced-motion` media query. When reduced motion is preferred, transitions and animations are minimised or removed. |

## 3. Functional Requirements

### 3.1 Semantic Structure

- All pages must use a logical heading hierarchy (one `<h1>` per page, followed by `<h2>`, `<h3>`, etc.) with no skipped levels.
- Navigation, main content, and complementary regions must use appropriate landmark elements (`<nav>`, `<main>`, `<aside>`, `<header>`, `<footer>`).
- Lists of items (categories, word cards, search results) must use semantic list markup (`<ul>`, `<ol>`, `<li>`).

### 3.2 Keyboard Navigation

- Every interactive element must be focusable and operable with keyboard alone (Enter, Space, Arrow keys, Escape as appropriate).
- A visible focus indicator must be present on the currently focused element at all times. The indicator must have sufficient contrast (3:1 against adjacent colours).
- Modal dialogs (e.g., host selection panel) must trap focus within the dialog while open and return focus to the triggering element on close.
- Skip-to-content links must be provided to bypass repeated navigation on every page.

### 3.3 Images & Media

- All informational images (host portraits, icons, progress indicators) must have descriptive `alt` text.
- Decorative images must have `alt=""` so they are ignored by assistive technology.
- Audio playback controls (play/replay word pronunciation) must have accessible labels (e.g., "Play pronunciation of _ciao_").
- Audio controls must be keyboard-operable (Space or Enter to play/pause).

### 3.4 Forms & Inputs

- Every form field (login, registration, word contribution, search) must have a visible label programmatically associated with the input, or an `aria-label` attribute when a visible label is not feasible (e.g., search inputs with placeholder text).
- Validation errors must be announced to screen readers via `aria-describedby` or live regions, and must not rely solely on colour to indicate an error.
- Required fields must be indicated both visually and programmatically (`aria-required="true"` or the `required` attribute).
- Form submission error messages (e.g., login failures, registration errors) must use `role="alert"` so that screen readers announce them immediately when they appear.
- The Add Word form must associate each input with its label via `htmlFor`/`id` pairing and must announce validation errors using `aria-describedby` with `role="alert"` elements.

### 3.5 Colour & Contrast

- Text contrast must meet WCAG AA minimums: 4.5:1 for normal-size text, 3:1 for large text (≥ 18pt or ≥ 14pt bold).
- Host colour-accent banners must not place text on a background that fails contrast requirements.
- Interactive components (buttons, links, form borders) and meaningful graphical elements must meet 3:1 contrast against their background.
- Information must never be conveyed by colour alone (e.g., progress indicators must also use text or icons).

### 3.6 Dynamic Content & Live Regions

- SPA route changes must be announced to screen readers using an `aria-live="polite"` region that reads the heading of the new page after each navigation event.
- Search-as-you-type results must announce the number of results to screen readers (e.g., "5 results found").
- Reference language switching must announce completion (e.g., "Language changed to Danish").
- Progress updates after playing a word must be perceivable by assistive technology without requiring the user to manually check.
- Error and success toasts must use `role="alert"` or `aria-live="assertive"`.

### 3.7 Motion & Animation

- All non-essential animations must respect the user's `prefers-reduced-motion` setting.
- No content should flash more than three times per second.

## 4. Edge Cases

- If a host persona portrait image fails to load, the alt text must still convey the host's name and language.
- If TTS audio generation fails and a word has no audio, the play button must indicate "Audio unavailable" rather than appearing silently broken.
- Extremely long user-contributed words must not break the layout or cause overflow that hides content from screen readers.

## 5. Dependencies

- Every existing FRD (F-AUDIO, F-AUTH, F-DICT, F-HOSTS, F-LANG, F-PROGRESS, F-SEARCH, F-UGC, F-EXAMPLES) must conform to the standards in this document.
- Accessibility requirements apply to all future features as well.

## 6. Acceptance Criteria

- [x] Audio playback controls have accessible labels with word name (e.g., "Play pronunciation of _ciao_"), are keyboard-operable, and have visible focus rings.
- [x] SPA route changes are announced via `aria-live="polite"` region.
- [x] Add Word form has full label association (`htmlFor`/`id`), required indicators, `aria-describedby` for errors, and `role="alert"` for submission errors.
- [ ] Login and Register page error messages use `role="alert"` for immediate screen-reader announcement. *(REM-1 — post-launch)*
- [ ] Search input has an `aria-label` when no visible `<label>` element is present. *(REM-2 — post-launch)*
- [ ] All pages pass automated WCAG 2.1 AA checks (e.g., axe-core with zero violations). *(REM-6 — pre-launch sweep recommended)*
- [ ] A manual keyboard-only walkthrough of every core flow (login → host selection → browse categories → play word → search → contribute word → view progress) completes without any keyboard traps or unreachable elements.
- [ ] A screen-reader walkthrough (NVDA on Windows or VoiceOver on macOS/iOS) of the same core flows is comprehensible — every element is labelled, every state change is announced.
- [ ] Colour contrast is verified for all host accent colours, buttons, text, and form elements.
- [ ] The site is usable at 200% browser zoom with no horizontal scrolling on a 1280px viewport.
- [ ] `prefers-reduced-motion` is respected: enabling it removes or reduces all transitions and animations.
- [ ] The Farah persona walkthrough (from the User Review Panel) surfaces no blocker or significant issues.
