# Task 049: Frontend Error Reporting UI

**Feature:** F-CONTENT-QA (Content Quality Assurance)
**Priority:** P1
**Dependencies:** 048 (ContentReport Data Model & API), 033 (Frontend Story Library), 009 (Frontend Categories & Words)

## Description

Add error reporting UI components to the story reading view, translation panel, and word cards so learners can flag content issues (grammar errors, wrong translations, pronunciation problems) without leaving the learning flow. The report form is lightweight — a category selector and optional free-text — designed to minimise disruption to the learning experience.

## Technical Requirements

### Report Button Placement

Add a report/flag button (flag icon or "Report" label) to these locations:

1. **Story reading view** — A small flag icon in the story header area (near the title or controls). Reports the story as a whole.
2. **Translation panel** — A small flag icon within the translation result area. Reports the specific word entry shown in the panel.
3. **Word card (Categories view)** — A small flag icon on each word card. Reports the specific word entry.

### Report Button Behaviour

- Tapping the report button opens a **lightweight modal or bottom sheet** with the report form
- The form auto-populates:
  - `content_type`: `"story"` or `"word"` based on where the button was tapped
  - `content_id`: the story ID or word ID of the current item
- User sees the item context (story title or word text) at the top of the form

### Report Form

- **Error category** — Required, single-select from:
  - Grammar / Spelling
  - Wrong Translation
  - Pronunciation Issue
  - Formatting Issue
  - Other
- **Description** — Optional text area, max 500 characters, with character counter
- **Submit button** — Sends `POST /api/reports` with the form data
- **Cancel button** — Closes the form without submitting

### Report Submission Flow

1. User taps submit
2. Frontend sends `POST /api/reports`
3. On success (201): close the form, show a brief toast notification ("Thanks for reporting — we'll review this")
4. On duplicate (409): show message "You've already reported this item. We'll review it soon." and close the form
5. On rate limit (429): show message "Too many reports. Please try again later."
6. On auth error (401): redirect to login (should not happen if UI is properly gated)
7. On validation error (422): show inline validation messages

### Visual Design

- Report button should be small and unobtrusive — it should not distract from learning
- Use a flag icon (`FlagIcon` from Heroicons or similar) as the primary icon
- Button colour: muted/grey by default, accent colour on hover
- The form modal/sheet should match the app's existing modal styles
- Category options displayed as radio buttons or a button group for quick selection

### Accessibility

- Report button must have an accessible label: `aria-label="Report an error"`
- Form elements must have proper labels and be keyboard-navigable
- Toast notification must be announced to screen readers (use `role="status"` or `aria-live="polite"`)
- Modal must trap focus while open and return focus to the trigger button on close

### i18n

Add translatable strings for:
- Report button label
- Form title ("Report an error")
- Category labels (Grammar / Spelling, Wrong Translation, Pronunciation Issue, Formatting Issue, Other)
- Description placeholder
- Submit/Cancel button labels
- Success/error toast messages
- Character counter format

## Acceptance Criteria

- [ ] Report button appears on story reading view, translation panel, and word cards
- [ ] Tapping report button opens form with auto-populated content type and ID
- [ ] Form has category selector (5 options) and optional description field
- [ ] Description field enforces 500-character limit with counter
- [ ] Successful submission closes form and shows confirmation toast
- [ ] Duplicate report shows appropriate message
- [ ] Rate limit shows appropriate message
- [ ] Report button is unobtrusive and does not distract from learning
- [ ] Form is fully keyboard-navigable and accessible to screen readers
- [ ] All strings are translated via i18next (en, da, it)

## Testing Requirements

- Report button is visible on story reading view
- Report button is visible on translation panel when a word is selected
- Report button is visible on word cards in categories view
- Clicking report opens the form with correct auto-populated fields
- Selecting a category and submitting sends correct API request
- Successful submission shows toast and closes form
- Duplicate report (409) shows appropriate message
- Form validates required category selection before submit
- Description character counter updates correctly
- Form is keyboard-navigable (Tab through fields, Enter to submit, Escape to close)
