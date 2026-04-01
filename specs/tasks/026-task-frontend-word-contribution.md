# Task 026: Frontend User Word Contribution

**Feature:** F-UGC (User-Contributed Words)
**Priority:** P1
**Dependencies:** 022 (User-Contributed Words API), 025 (Frontend Multi-Language Dictionary)

## Description

Implement the frontend UI for users to contribute new words to the shared dictionary. This includes a word submission form accessible from the main navigation, input validation, feedback on submission success or duplicate detection, and immediate integration of the new word into the browsing experience.

## Technical Requirements

### Add Word Page/Modal
- A dedicated page or modal accessible via an "Add Word" button on the categories page and/or in the navigation
- The form includes:
  - **Word** (required, text input) — the word in the current target language, with a label reflecting the target language (e.g., "Italian word", "Danish word")
  - **Translation** (required, text input) — translation in the user's current reference language, with a label reflecting the reference language
  - **Phonetic hint** (optional, text input) — pronunciation guide
  - **Category** (optional, dropdown) — list of existing categories plus "Uncategorised" default
  - **Difficulty** (optional, select) — Beginner (default) / Intermediate / Advanced
  - **Example sentence** (optional, text input) — an example in the target language
  - **Example translation** (optional, text input) — translation of the example in the reference language
- Submit button with loading state

### Validation
- Client-side validation: word must be non-empty, max 100 characters
- Translation must be non-empty
- Display inline validation errors

### Submission Flow
- On submit, call `POST /api/dictionary/words` with the form data
- On success: display a success message, clear the form, and optionally navigate to the new word's category
- On 409 (duplicate): display a message indicating the word already exists, with a link to the existing word
- On 400 (validation error): display the server's error message
- On error: display a generic error message

### API Service
- Add a `contributeWord()` function to the API service module
- The function sends the form data to `POST /api/dictionary/words`

### i18n
- All form labels, validation messages, success/error messages must be translatable
- Add the necessary keys to `en.json`, `da.json`, and `it.json`

## Acceptance Criteria

- [ ] An "Add Word" button is visible on the categories page
- [ ] The word submission form displays with all required and optional fields
- [ ] Client-side validation prevents empty word or translation submission
- [ ] Successful submission creates the word and shows a success message
- [ ] Duplicate words show a 409 error with a link to the existing word
- [ ] The new word appears in the dictionary immediately after contribution
- [ ] All form labels and messages are translated in all three languages
- [ ] The form is responsive and accessible (touch targets, focus management)

## Testing Requirements

- Form renders with all expected fields
- Submit button is disabled when required fields are empty
- Successful submission calls the API and shows success feedback
- Form displays duplicate error for 409 responses
- Form displays validation error for 400 responses
- i18n keys exist for all form labels and messages
