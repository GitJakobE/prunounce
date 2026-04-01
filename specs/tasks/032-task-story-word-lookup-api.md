# Task 032: Story Word Lookup API

**Feature:** F-STORY (Story Reading)
**Priority:** P1
**Dependencies:** 029 (Story Data Model & API), 005 (Backend Dictionary Search)

## Description

Implement a single-word lookup endpoint that enables the story reading view's tap-to-translate functionality. When a user taps a word in a story, the frontend tokenises the click target and sends the normalised word to this endpoint. The backend performs an exact-match lookup against the dictionary after normalising the input (stripping punctuation, lowercasing). If the word exists, its translation and audio pronunciation are returned; if not, a "Translation not available" response is returned.

## Technical Requirements

### Lookup Endpoint

- `GET /api/dictionary/lookup` — look up a single word for translation
  - Query parameters:
    - `word` — the word to look up (required, string)
    - `lang` — the target language code (`it`, `da`, `en`) (required)
  - Returns JSON:
    - On match: `{ found: true, word: { id, word, translation, categoryId } }`
    - On no match: `{ found: false, word: null }`
  - Translation is returned in the user's reference language (same column-per-language pattern)
  - Protected by auth middleware

### Normalisation

- Strip leading and trailing punctuation (.,;:!?'"()-— etc.)
- Convert to lowercase
- Trim whitespace
- Handle Unicode punctuation (e.g., Italian « » guillemets, Danish quotation marks)
- After normalisation, perform exact match against the `Word.word` column (which stores lowercase canonical forms)

### Frontend Tokenisation Guidance (for task 034)

- The frontend is responsible for tokenising on click — splitting the story body by whitespace and punctuation to identify the clicked word
- The frontend should strip punctuation before sending to this endpoint
- This task only implements the backend; frontend integration is in task 034

### Performance

- Single-word lookup should be a fast indexed query
- Ensure the `Word.word` column is indexed (or verify existing index)

## Acceptance Criteria

- [ ] `GET /api/dictionary/lookup?word=X&lang=Y` returns the word's translation when found
- [ ] Returns `{ found: false }` when the word is not in the dictionary
- [ ] Punctuation is stripped before matching (e.g., `"ciao!"` matches `ciao`)
- [ ] Lookup is case-insensitive
- [ ] Translation is returned in the user's reference language
- [ ] Invalid or missing `word` parameter returns 400
- [ ] Invalid or missing `lang` parameter returns 400
- [ ] 401 is returned for unauthenticated requests

## Testing Requirements

- Exact match returns correct word and translation
- Word with surrounding punctuation is normalised and matched
- Word with mixed case is normalised and matched
- Non-existent word returns `{ found: false }`
- Empty word parameter returns 400
- Missing lang parameter returns 400
- Invalid lang code returns 400
- Unauthenticated request returns 401
- Translation returned matches the user's reference language preference
