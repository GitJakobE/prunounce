# Task 041: Accessibility Manual Audit & Remediation

**Feature:** F-A11Y (Accessibility & Inclusive Design)
**Priority:** P0 (Release blocker per review panel — Farah verdict: fail)
**Dependencies:** 015 (Responsive & Accessibility — initial pages), 036 (Story Accessibility), 037 (Multilang/UGC Accessibility)
**Review reference:** [2026-03-29 review](../reviews/2026-03-29-current-state.md) — CUT-3
**ADRs:** ADR-0021 (Accessibility Testing)

## Problem

The 2026-03-29 review panel could not clear three significant accessibility unknowns via API probing alone. These must be verified and fixed through manual browser testing with keyboard-only navigation and a screen reader before any public launch.

### Specific unknowns

1. **`AudioButton` ARIA labels** — The component exists (`AudioButton.tsx`) but its `aria-label`, `aria-pressed`, and `role` attributes have not been verified. This is the primary interactive element of the entire app.

2. **SPA route-change announcements** — `App.tsx` uses React Router client-side navigation. Without an `aria-live` region or focus management after route changes, screen reader users may not know the page changed (e.g., after host selection redirects to `/`).

3. **`AddWordPage` form accessibility** — Field `<label>` elements, required-field announcements, inline error association via `aria-describedby`, and form submission feedback have not been confirmed.

## Requirements

### 1. AudioButton audit and fix

- Verify `AudioButton.tsx` has:
  - `aria-label` that includes the word being pronounced (e.g., `"Play pronunciation of ciao"`)
  - `aria-label` for the example sentence variant (e.g., `"Play example sentence for ciao"`)
  - A visible focus ring on keyboard focus
  - Activation via Enter and Space keys
- If any are missing, add them

### 2. SPA route-change announcements

- Implement a route-change announcer that communicates page transitions to screen readers
- Options:
  - An `aria-live="polite"` region that announces the new page title after each `useLocation()` change
  - Focus management: move focus to the `<h1>` of the new page after navigation
- Must cover at least: login → register, register → select-host, select-host → categories, categories → category detail, any page → search, any page → profile, any page → add-word, any page → stories, stories → story reading

### 3. AddWordPage form audit and fix

- Every `<input>` and `<select>` must have a visible `<label>` with matching `for`/`id`
- Required fields must communicate "required" to assistive technology (either via `aria-required="true"` or `required` attribute)
- Validation error messages must be associated with their field via `aria-describedby`
- On submission success, announce "Word added successfully" via an `aria-live` region
- On submission failure, announce the error message via an `aria-live` region

### 4. Smoke test with axe-core

- Run axe-core via browser DevTools on every page and fix any critical or serious violations:
  - `/login`
  - `/register`
  - `/select-host`
  - `/` (categories)
  - `/categories/:id` (word detail)
  - `/search`
  - `/add-word`
  - `/profile`
  - `/stories`
  - `/stories/:id` (story reading)

## Acceptance Criteria

- [ ] `AudioButton` has `aria-label` including the word name on every instance
- [ ] `AudioButton` is keyboard-activatable (Enter / Space) with visible focus ring
- [ ] Route changes are announced to screen readers (via `aria-live` region or focus management)
- [ ] All `AddWordPage` form fields have programmatically associated labels
- [ ] Required fields communicate "required" to assistive technology
- [ ] Validation errors are associated with their fields via `aria-describedby`
- [ ] Form success/failure is announced via `aria-live` region
- [ ] axe-core reports zero critical or serious violations on all 10 pages
- [ ] All fixes verified with NVDA (Windows) or VoiceOver (macOS) screen reader

## Testing Requirements

- Run axe-core on each page and capture results (zero critical/serious violations)
- Keyboard-only walkthrough: Tab through every page, confirm all interactive elements reachable
- Screen reader test: navigate login → register → select host → categories → word detail → search → add word → profile → stories → story reading; confirm each transition is announced
- AudioButton: confirm screen reader reads the word name when focused
- AddWordPage: confirm screen reader reads field labels, required status, and error messages
