# Task 061: On-the-Fly Lookup Integration Testing

**Feature:** F-OTFLOOKUP (On-the-Fly Word Lookup & Audio)
**Priority:** P2
**Dependencies:** 056, 057, 058, 059, 060 (all prior OTF tasks)

## Description

Add integration and end-to-end tests that verify the full on-the-fly word lookup and audio pipeline works correctly across the backend API layer. These tests exercise the cascade from curated lookup through translation cache to external translation, as well as the pronounce audio endpoint, rate limiting, and error scenarios.

## Technical Requirements

### Backend Integration Tests

Create test files in `src/backend-python/tests/` covering the following scenarios.

#### Lookup Cascade (`GET /api/dictionary/lookup`)

1. **Curated hit:** Seed a `Word` row, call lookup → returns `source="curated"` with correct translation
2. **Cache hit:** Seed a `TranslationCache` row (no matching `Word`), call lookup → returns `source="cached"`
3. **External translation (mocked):** No `Word` or cache row, mock `GoogleFreeTranslationProvider.translate()` to return a string → returns `source="auto-translated"` and a new `TranslationCache` row exists
4. **External failure (mocked):** Mock provider to return `None` → returns `source="none"`, `translation=None`, no cache row created
5. **Cascade order:** Mock both DB and provider, verify curated is checked before cache before external
6. **Repeat call after auto-translate:** First call auto-translates and caches; second call returns `source="cached"` without hitting external provider

#### Pronounce Audio (`GET /api/audio/pronounce`)

7. **Valid request:** Call with valid word + lang → returns 200 with `audio/mpeg` content type
8. **Input validation — oversized:** Word > 100 chars → 400
9. **Input validation — invalid chars:** Word with `<script>` → 400
10. **Input validation — bad lang:** `lang=xx` → 400
11. **Rate limit:** Send 61 requests in rapid succession → 60 succeed, 61st returns 429
12. **Auth required:** No token → 401
13. **TTS failure (mocked):** Mock `get_audio_path` to return `None` → 503

#### Translation Caching

14. **Concurrent inserts:** Two concurrent requests for the same uncached word → both succeed; only one `TranslationCache` row created (no `IntegrityError`)
15. **Cache isolation:** Translating "ciao" it→en and "ciao" it→da create separate cache entries

#### Cross-Language

16. **All language pairs:** Verify lookup works for it→en, it→da, en→it, en→da, da→it, da→en (mocked provider)

### Test Setup

- Use the existing test infrastructure (pytest, `TestClient`, fixtures from `conftest.py`)
- Mock external translation calls (never call real Google Translate in tests)
- Mock TTS generation for audio tests (avoid slow edge-tts calls)
- Use temporary SQLite databases (existing pattern) so tests are isolated

## Acceptance Criteria

- [ ] All 16 test scenarios pass
- [ ] No real external API calls (translation or TTS) in the test suite
- [ ] Tests run in < 30 seconds total
- [ ] Tests are isolated — no cross-test state leakage
- [ ] Coverage for error paths (provider failure, invalid input, rate limit, auth)
- [ ] Coverage for the full cascade ordering

## Testing Requirements

This task IS the testing task — all items above are the tests that must be written and passing.
