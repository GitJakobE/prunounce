# Task 022: User-Contributed Words API

**Feature:** F-UGC (User-Contributed Words)
**Priority:** P1
**Dependencies:** 017 (Schema Migration), 019 (Multi-Language Dictionary API), 021 (Multi-Language Audio)

## Description

Implement the backend API endpoint for users to contribute new words to the shared dictionary. The endpoint accepts a word in the current target language with at least one translation, validates against duplicates, saves the word, and triggers asynchronous TTS audio generation.

## Technical Requirements

### API Endpoint
- `POST /api/dictionary/words` — create a new user-contributed word
- Request body:
  - `word` (required, string) — the word in the target language
  - `translation` (required, string) — translation in the user's current reference language
  - `phoneticHint` (optional, string) — pronunciation guide
  - `categoryId` (optional, string) — category to assign the word to
  - `difficulty` (optional, string) — defaults to `"beginner"`
  - `example` (optional, string) — example sentence in the target language
  - `exampleTranslation` (optional, string) — example sentence translation in the reference language
- Protected by auth middleware

### Validation
- Word text must be non-empty, max 100 characters
- Word must not contain only whitespace, numbers, or special characters
- Duplicate check: case-insensitive match on `[word, language]` unique constraint. If duplicate found, return 409 with the existing word's ID
- Translation text must be non-empty
- Difficulty must be one of: `"beginner"`, `"intermediate"`, `"advanced"`
- Category ID (if provided) must reference an existing category

### Word Creation
- Set `language` from the user's current target language (resolved from host)
- Set `source = "user"`
- Set `contributedBy` to the authenticated user's ID
- Set the translation in the appropriate reference language column; leave other translation columns empty (or set to the provided translation as a fallback)
- If category is provided, create the WordCategory association
- If category is not provided, assign to an "Uncategorised" category (create this category if it doesn't exist)

### Audio Generation
- After saving the word, trigger TTS audio generation asynchronously
- Use the contributing user's current host voice
- Generate audio for both the word and the example sentence (if provided)
- The word should be usable immediately even if audio generation is still in progress

### Response
- Return the created word with its ID, translations, and a flag indicating audio generation status

## Acceptance Criteria

- [ ] `POST /api/dictionary/words` creates a new word in the user's target language
- [ ] The word appears in dictionary and search results for all users
- [ ] Duplicate word+language combinations are rejected with 409
- [ ] Validation rejects empty words, words over 100 chars, and invalid difficulty values
- [ ] The word is tagged with `source = "user"` and `contributedBy = userId`
- [ ] Audio is generated asynchronously after word creation
- [ ] Words without a category are assigned to "Uncategorised"
- [ ] The endpoint returns 401 for unauthenticated requests

## Testing Requirements

- Valid word submission creates a word record with correct language and source
- Duplicate word returns 409 with existing word ID
- Empty or whitespace-only word is rejected with 400
- Word over 100 characters is rejected with 400
- Invalid difficulty value is rejected with 400
- Invalid category ID is rejected with 400
- Word is visible in dictionary listing and search after creation
- Unauthenticated requests return 401
