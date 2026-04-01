# Task 019: Multi-Language Dictionary API

**Feature:** F-DICT (Word Dictionary), F-LANG (Multi-Language Learning)
**Priority:** P0
**Dependencies:** 017 (Schema Migration), 018 (Expand Hosts)

## Description

Update all dictionary and search API endpoints to operate on a target-language word set determined by the user's chosen host. Currently the API assumes all words are Italian. After this task, the API filters words by the target language derived from the user's host selection and serves translations in the requested reference language.

## Technical Requirements

### Target Language Resolution
- Determine the user's target language from their saved `hostId` preference, by looking up the host's `language` field
- All dictionary queries must filter by `Word.language = targetLanguage`

### Dictionary Endpoints Update
- `GET /api/dictionary/categories` — filter word counts and progress to only include words matching the user's target language. Accept `?lang=en|da|it` for reference language (excluding the target language).
- `GET /api/dictionary/categories/:id/words` — return only words in the user's target language. Map the `word` column instead of the old `italian` column. Serve translation from the appropriate reference language column. Include `exampleTarget` (the example in the target language) and `example` (the example in the reference language).

### Search Endpoint Update
- `GET /api/search?q=<term>&lang=<ref>` — search in the target language's word column AND the reference language's translation column. Only search within words matching the user's target language.

### Category Name Localisation
- Return category names in the user's reference language: `lang=en` → `nameEn`, `lang=da` → `nameDa`, `lang=it` → `nameIt`

### Reference Language Validation
- Validate that the requested reference language is not the same as the target language
- If `lang` is omitted, default to `"en"` (unless target language is English, then default to `"da"`)

### Response Shape
- Replace any `italian` field in API responses with a generic `word` field
- The frontend must receive the word in the target language as `word`, not `italian`

## Acceptance Criteria

- [ ] Dictionary endpoints filter words by the user's target language
- [ ] An Italian-host user sees only Italian words; a Danish-host user sees only Danish words
- [ ] Reference language parameter controls which translation is returned
- [ ] Category names are returned in the reference language
- [ ] Search operates within the correct target language word set
- [ ] Search matches against both the target-language word and reference-language translation
- [ ] The `italian` field is replaced by `word` in all API responses
- [ ] Example sentences are served in both target and reference languages
- [ ] All existing tests are updated and pass

## Testing Requirements

- Dictionary returns Italian words for a user with an Italian host
- Dictionary returns Danish words for a user with a Danish host
- Reference language parameter switches translation and category name language
- Search finds words by target-language query
- Search finds words by reference-language translation query
- Requesting reference language = target language returns a validation error (or uses fallback)
- Progress counts are scoped to the target language's words
