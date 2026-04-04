# Task 057: Translation Service with Provider Abstraction

**Feature:** F-OTFLOOKUP (On-the-Fly Word Lookup & Audio)
**Priority:** P1
**Dependencies:** 056 (TranslationCache Model)

## Description

Implement a translation service layer that translates individual words using an external translation provider when they are not found in the curated dictionary. The service must follow the same provider-abstraction pattern used by the TTS service (`TTSProvider` ABC in `app/services/tts.py`), with `deep-translator` as the default implementation using Google Translate's free endpoint. The service must handle errors gracefully and never cache failed results.

## Technical Requirements

### Provider Abstraction

- Create a `TranslationProvider` ABC in `app/services/translation.py`
- Abstract method: `translate(text: str, source_lang: str, target_lang: str) -> str | None`
  - Returns the translated text on success, `None` on failure
  - `source_lang` and `target_lang` use ISO 639-1 codes (`it`, `en`, `da`)

### Google Free Translation Provider

- Implement `GoogleFreeTranslationProvider` using the `deep-translator` library
- Use `GoogleTranslator` from `deep-translator` as the default backend
- Must support all six language-pair directions: it↔en, it↔da, en↔da (and reverses)
- Handle exceptions from the translation library (network errors, rate limits, invalid responses) — return `None` on any failure
- Log errors but do not raise exceptions to callers

### Dependency Addition

- Add `deep-translator` to `pyproject.toml` dependencies

### Cache Integration

- The service must check the `TranslationCache` table before calling the external provider
- On a cache hit, return the cached translation immediately
- On a cache miss + successful external translation, insert the result into `TranslationCache`
- On a cache miss + failed external translation, return `None` without caching
- The `TranslationCache` lookup and insert must use the unique constraint `(word, sourceLang, targetLang)` — handle `IntegrityError` on concurrent inserts gracefully (treat as cache hit)

### Service Interface

- Expose a high-level function (e.g., `translate_word(word: str, source_lang: str, target_lang: str, db: Session) -> str | None`) that encapsulates the cache-check → external-call → cache-write flow
- This function is what the lookup endpoint will call

## Acceptance Criteria

- [ ] `TranslationProvider` ABC exists with `translate()` method
- [ ] `GoogleFreeTranslationProvider` implements the ABC using `deep-translator`
- [ ] `deep-translator` added to `pyproject.toml`
- [ ] Translation succeeds for all six language pair directions (it↔en, it↔da, en↔da)
- [ ] External translation errors return `None` without raising exceptions
- [ ] `translate_word()` checks `TranslationCache` before calling the external provider
- [ ] Successful translations are persisted to `TranslationCache`
- [ ] Failed translations are NOT persisted to `TranslationCache`
- [ ] Concurrent inserts for the same word/language pair do not raise errors
- [ ] Errors are logged with sufficient context for debugging

## Testing Requirements

- Successful translation returns expected text for each language pair
- External provider failure returns `None`
- Cache hit returns stored translation without calling external provider (verify with mock)
- Cache miss calls external provider, stores result, subsequent call returns from cache
- Failed translation is not stored in cache — a retry calls the external provider again
- Concurrent cache writes for the same key do not raise errors
- Invalid language codes are handled gracefully (return `None`)
