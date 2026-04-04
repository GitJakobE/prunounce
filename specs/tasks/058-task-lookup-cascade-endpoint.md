# Task 058: Lookup Cascade Endpoint

**Feature:** F-OTFLOOKUP (On-the-Fly Word Lookup & Audio)
**Priority:** P1
**Dependencies:** 056 (TranslationCache Model), 057 (Translation Service)

## Description

Extend the existing `GET /api/dictionary/lookup` endpoint with a three-step cascade so that words not found in the curated `Word` table are automatically translated on the fly using the translation service from task 057. The endpoint must add a `source` field to `WordLookupResult` so the frontend can distinguish curated translations from auto-translated ones.

## Technical Requirements

### Schema Change — `WordLookupResult`

- Add a `source` field to `WordLookupResult` in `app/schemas.py`:
  ```python
  class WordLookupResult(BaseModel):
      word: str
      translation: str | None
      phoneticHint: str | None
      wordId: str | None
      source: str  # "curated" | "cached" | "auto-translated"
  ```
- `"curated"` — found in the `Word` table
- `"cached"` — found in the `TranslationCache` table
- `"auto-translated"` — freshly translated by the external provider (then cached)

### Three-Step Lookup Cascade

Modify `lookup_word()` in `app/routers/dictionary.py`:

1. **Step 1 — Curated lookup (existing behaviour):**
   Query the `Word` table for the normalised word. If found, return with `source="curated"`.

2. **Step 2 + Step 3 — Delegated to `translate_word()`:**
   Call `translate_word(word, source_lang=target_lang, target_lang=ref_lang, db=db)` from task 057, which already handles:
   - Checking `TranslationCache` (returns `source="cached"` equivalent)
   - Calling the external provider (returns `source="auto-translated"` equivalent)
   - Caching successes in `TranslationCache`

   The `translate_word()` function returns `(translation: str | None, source: str | None)` (adjust interface if needed), or the endpoint determines `source` based on the function's semantics.

3. **If all steps fail:**
   Return `WordLookupResult(word=word, translation=None, phoneticHint=None, wordId=None, source="none")`

### Language Parameter Semantics

Preserve existing semantics:
- `target_lang = resolve_user_target(user_id, db)` — the language the user is learning (e.g., `"it"`)
- `ref_lang = resolve_ref_lang(lang, target_lang, user_id, db)` — the user's reference/native language (e.g., `"en"`)
- For the translation cascade, translate **from** `target_lang` **to** `ref_lang`

### Performance

- The curated lookup step remains unchanged in behaviour
- The cascade adds latency only when the word is NOT in the Word table
- Target latencies: cached ≤ 1 s, uncached ≤ 3 s (per ADR-0027)

## Acceptance Criteria

- [ ] `WordLookupResult` schema includes `source` field
- [ ] Curated words return `source="curated"` with existing data intact
- [ ] Words found in `TranslationCache` return `source="cached"`
- [ ] Words not in either table trigger an external translation and return `source="auto-translated"`
- [ ] Auto-translated results are persisted to `TranslationCache` for future requests
- [ ] If translation fails, response has `translation=None` and `source="none"`
- [ ] Language parameters (`lang`, user target) are passed correctly through the cascade
- [ ] Existing curated-word lookup behaviour and performance are unaffected
- [ ] No regressions in existing `/api/dictionary/lookup` tests

## Testing Requirements

- Curated word lookup returns `source="curated"` (unit test with mocked DB)
- Cache hit returns `source="cached"` (unit test)
- Cache miss + successful translation returns `source="auto-translated"` and writes to cache (unit test with mocked provider)
- Cache miss + failed translation returns `source="none"` with `translation=None` (unit test)
- Full cascade ordering: curated checked first, then cache, then external (verify call order with mocks)
- Existing endpoint contract preserved for curated words (integration test)
