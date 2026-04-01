# Task 052: Accessibility ARIA Polish

**Feature:** F-A11Y (Accessibility & Inclusive Design)
**Priority:** P1
**Dependencies:** 041 (Accessibility Audit & Remediation)
**Review reference:** [2026-03-30 post-fix review](../reviews/2026-03-30-post-fix-review.md) — REM-1, REM-2
**ADRs:** ADR-0021 (Accessibility Testing)

## Problem

The 2026-03-30 post-fix review resolved all three CUT-3 accessibility blockers but identified two remaining minor ARIA gaps that prevent Farah (screen-reader persona) from achieving a clean pass:

1. **REM-1 — Login/Register error announcements:** `LoginPage.tsx` and `RegisterPage.tsx` display authentication error messages in a `<div>` but do not mark them with `role="alert"`. Screen readers (NVDA, VoiceOver) may not announce login/registration failures, leaving keyboard-only users unaware of errors.

2. **REM-2 — SearchPage input label:** `SearchPage.tsx` renders a search `<input>` with `placeholder` text but no `<label>` element or `aria-label` attribute. Screen readers may not identify the input's purpose.

## Requirements

### 1. Auth error announcement (REM-1)

- In `LoginPage.tsx`, add `role="alert"` to the error message container that renders when authentication fails
- In `RegisterPage.tsx`, add `role="alert"` to the error message container that renders when registration fails
- The error text must remain visible and styled as it is today — only the ARIA role is added
- Ensure screen readers announce the error message immediately when it appears

### 2. Search input label (REM-2)

- In `SearchPage.tsx`, add `aria-label={t("search.placeholder")}` to the search `<input>` element
- Alternatively, add a visually-hidden `<label>` element with a `for`/`id` pairing to the input
- The visual appearance of the search input must not change

### 3. Profile email label (supplementary)

- In `ProfilePage.tsx`, the email field is a disabled display-only input without a `htmlFor`/`id` pairing on its `<label>`
- Add the `htmlFor`/`id` pairing to maintain label association even though the field is non-interactive
- This is cosmetic from a usability standpoint but completes WCAG compliance for the page

## Acceptance Criteria

- [ ] Login error messages have `role="alert"` — screen readers announce auth failures immediately
- [ ] Register error messages have `role="alert"` — screen readers announce registration failures immediately
- [ ] SearchPage search input has `aria-label` or a visually-hidden `<label>` — screen readers identify the field
- [ ] ProfilePage email label has `htmlFor` matching the input's `id`
- [ ] Visual appearance of all affected pages is unchanged
- [ ] All existing frontend tests continue to pass
- [ ] axe-core reports zero critical or serious violations on `/login`, `/register`, `/search`, and `/profile`

## Testing Requirements

- **Unit tests:** Verify the `role="alert"` attribute is present on error containers in LoginPage and RegisterPage test files
- **Unit tests:** Verify SearchPage input has `aria-label` or an associated `<label>`
- **Screen reader verification:** Tab through login → enter bad credentials → confirm error is announced; repeat for register
- **Screen reader verification:** Tab to search input → confirm screen reader reads the label text
- **Regression:** Run `npx vitest --run` — all existing tests pass
- **axe-core:** Run on `/login`, `/register`, `/search`, `/profile` — zero critical/serious violations
