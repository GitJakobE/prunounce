# ADR-0027: Story Word Lookup Cascade & On-the-Fly Audio Endpoint

- **Status:** Proposed
- **Date:** 2026-04-02
- **Deciders:** Development team
- **Requirements:** REQ-18 (On-the-Fly Word Lookup & Audio), REQ-14 (Story Reading)
- **Extends:** [ADR-0013](0013-story-word-lookup.md) (Story Word Tokenisation & Dictionary Lookup)
- **Related:** [ADR-0025](0025-on-the-fly-translation-provider.md), [ADR-0026](0026-on-the-fly-translation-caching.md), [ADR-0007](0007-audio-delivery.md), [ADR-0016](0016-tts-provider-edge-tts.md)

## Context and Problem Statement

ADR-0013 defined a simple lookup endpoint: the frontend sends a clicked word, the backend does an exact match against the `Word` table, and returns either a match or `null`. This works for curated dictionary words but returns nothing for the majority of words in natural story text (conjugated verbs, articles, pronouns, declined nouns, common adverbs).

REQ-18 requires the lookup endpoint to be extended with a fallback cascade: try the curated dictionary first, fall back to an on-the-fly translation if no match, and cache the result. Additionally, on-the-fly words need an audio playback path — but they don't have a `wordId`, so they can't use the existing `GET /api/audio/:wordId` endpoint.

This ADR defines the extended lookup response, the fallback cascade, and the new audio endpoint for on-the-fly words.

## Decision Drivers

- The existing lookup endpoint (`GET /api/dictionary/lookup`) must continue to work for curated dictionary words — no regressions
- The cascade must be transparent to the frontend: one API call returns either a curated or auto-translated result
- The response must indicate the source (curated vs. auto-translated) so the frontend can render the indicator
- On-the-fly words need audio playback without a `wordId`
- Latency for the full cascade (dictionary miss → translation → cache write) must stay under 3 seconds
- The endpoint design should be clean and not require the frontend to make multiple sequential calls for the common case

## Considered Options

### Option 1: Extend existing lookup endpoint with cascade and add text-based audio endpoint (Chosen)

Modify the existing `GET /api/dictionary/lookup` endpoint to perform a three-step cascade:
1. Check curated dictionary (existing behaviour)
2. Check `TranslationCache` table
3. Call external translation service, cache result

Add a new `GET /api/audio/pronounce` endpoint that accepts raw word text and generates/serves audio on the fly.

### Option 2: Separate endpoint for on-the-fly lookups

Keep the existing lookup endpoint unchanged. Add a new `GET /api/dictionary/translate` endpoint that the frontend calls only after a dictionary miss. The frontend decides whether to call the second endpoint.

**Pros:**
- Existing endpoint unchanged — zero regression risk
- Clear separation of concerns

**Cons:**
- Frontend must make two sequential API calls for every non-dictionary word (dictionary miss → translate), doubling latency
- Frontend logic becomes more complex (must handle the cascade itself)
- Redundant network round-trips for the most common failure case

### Option 3: Pre-translate all story words at seed time

When a story is seeded, pre-process every word: look up in dictionary, translate if missing, and store all translations in a `StoryWordTranslation` table. Serve everything from the pre-computed table at read time.

**Pros:**
- Zero runtime latency for any story word
- Complete translation coverage guaranteed before users see the story

**Cons:**
- Tight coupling between stories and dictionary — any dictionary change requires reprocessing
- Translation table grows with every story × every reference language
- Requires a batch translation job in the seeding workflow
- Does not handle words the user might encounter outside the story context (future reuse blocked)
- Significantly larger seeding workflow and data volume

## Decision Outcome

**Chosen: Option 1 — Extend existing lookup endpoint with cascade and add text-based audio endpoint**

### Rationale

- Single API call from the frontend for any word — the backend handles the cascade internally
- The frontend rendering logic is simple: check `source` field in response, render accordingly
- Reuses the existing endpoint path — no frontend routing changes for the primary lookup
- The text-based audio endpoint is a clean addition that does not conflict with the existing `wordId`-based endpoint
- Pre-translation (Option 3) is over-engineered and couples stories to the translation pipeline

### Extended Lookup Endpoint

**Endpoint:** `GET /api/dictionary/lookup?word={word}&lang={language}`

This is the same endpoint defined in ADR-0013, extended with additional cascade steps.

**Cascade logic (backend):**

```
1. Resolve target language from user's host (existing: resolve_user_target())
2. Resolve reference language from `lang` parameter or user profile (existing: resolve_ref_lang())
3. Normalise the word (lowercase, strip diacriticals)
4. Query the Word table (exact match on word + target language)
   → If found: return curated result with source="curated"
5. Query the TranslationCache table (word + target language + reference language)
   → If found: return cached auto-translation with source="auto-translated"
6. Call external translation service (ADR-0025)
   → If successful:
     a. Insert into TranslationCache
     b. Return result with source="auto-translated"
   → If failed: return result with translation=null, source=null
```

The **target language** (the language the story word is in) is always resolved from the user's currently selected host — consistent with the existing `resolve_user_target()` function. The optional `lang` query parameter serves as a **reference language override** — if omitted, the reference language is read from the user's profile. This matches the existing endpoint contract.

**Extended response (curated match):**
```json
{
  "word": "buongiorno",
  "translation": "good morning",
  "phoneticHint": "bwon-JOHR-noh",
  "wordId": "uuid-here",
  "source": "curated"
}
```

**Extended response (auto-translated):**
```json
{
  "word": "chiamo",
  "translation": "I call",
  "phoneticHint": null,
  "wordId": null,
  "source": "auto-translated"
}
```

**Extended response (all lookups failed):**
```json
{
  "word": "xyzzy",
  "translation": null,
  "phoneticHint": null,
  "wordId": null,
  "source": null
}
```

**Schema change required:** The `source` field is a new addition. Both the backend Pydantic model (`WordLookupResult` in `app/schemas.py`) and the frontend TypeScript type (`WordLookupResult` in `src/types/index.ts`) must be updated to include `source: string | null`. Existing consumers that do not use `source` are unaffected — the field is additive.

The frontend uses the `source` field to decide:
- `"curated"` → standard display, audio via `GET /api/audio/{wordId}`
- `"auto-translated"` → show "auto-translated" indicator, audio via `GET /api/audio/pronounce?word={word}&lang={language}`
- `null` → show "Translation temporarily unavailable"

### Text-Based Audio Endpoint

**Endpoint:** `GET /api/audio/pronounce?word={word}&lang={language}`

This new endpoint serves pronunciation audio for words that are not in the curated dictionary and therefore have no `wordId`. The path uses `/pronounce` rather than `/text` to avoid route ambiguity with the existing `GET /api/audio/{word_id}` path parameter route — FastAPI would otherwise attempt to match the literal `"text"` as a `word_id`.

**Behaviour:**
1. Authenticate the request (same token mechanism as ADR-0007)
2. Resolve the user's current host and its TTS voice
3. Validate that the host's language matches the `lang` parameter (the target language the word belongs to)
4. Call `get_audio_path(word, None, host_id, voice_name)` — the existing TTS function generates on cache miss and caches the result
5. Return the audio file with the same headers as the existing audio endpoint

**Important:** This route must be registered **before** the `/{word_id}` route in the FastAPI router to ensure it takes priority over the path parameter capture.

**Security considerations:**
- The `word` parameter must be length-limited (max 100 characters) to prevent abuse of the TTS service
- The `word` parameter must be sanitised — only Unicode letters (including accented characters such as à, è, é, ì, ò, ù, æ, ø, å), spaces, hyphens, and apostrophes are accepted. Use a regex like `^[\p{L}\s'\-]+$` with the `regex` library or equivalent Unicode-aware pattern.
- A dedicated rate limiter must be added for this endpoint (the existing `rate_limit.py` is login-specific and cannot be reused). A simple in-memory per-user limiter (e.g., max 60 requests/minute per authenticated user) is sufficient for v1.
- The endpoint requires authentication (same as all other audio endpoints)

**Cache key:** `{sanitize_filename(word)}_{host_id}.mp3` — identical to curated word audio files. If a curated word and an on-the-fly word share the same text, they naturally share the same cached audio file.

**Note:** The existing `sanitize_filename()` in `tts.py` allows `àèéìòùæøåäöüß` but should be verified to cover all Unicode letters that appear in story text across all three languages.

### Latency Budget

The 3-second requirement (REQ-18) applies to the combined cascade when both translation and audio are uncached:

| Step | Estimated Latency |
|---|---|
| Dictionary lookup (cache miss) | ~1 ms |
| TranslationCache lookup (cache miss) | ~1 ms |
| External translation call (ADR-0025) | ~200–500 ms |
| TTS generation via Edge TTS (ADR-0016) | ~1–3 s |
| **Total (worst case)** | **~1.2–3.5 s** |

The worst case slightly exceeds 3 seconds. Mitigations:
- Translation and TTS generation can be executed **in parallel** — the translation result is not needed for pronunciation. The audio endpoint is called separately by the frontend after the lookup response returns, so the two operations naturally overlap.
- With parallel execution, effective latency = max(translation, TTS) ≈ 1–3 seconds, within budget.
- If TTS alone exceeds 3 seconds (rare, ~first retry), the 3-second target is a P95 goal, not a hard guarantee — consistent with ADR-0016's note that first-play latency is 1–3 seconds.

### Frontend Changes

The frontend story reading view changes are minimal:

1. **Lookup call:** No URL change — same `GET /api/dictionary/lookup` endpoint
2. **Response handling:** Check the new `source` field:
   - If `source === "curated"`: render as today (no indicator, audio via `/api/audio/{wordId}`)
   - If `source === "auto-translated"`: show "auto-translated" label below translation, audio via `/api/audio/pronounce?word={word}&lang={language}`
   - If `source === null`: show "Translation temporarily unavailable"
3. **Session cache:** The existing `Map<string, LookupResult>` caches all results regardless of source
4. **Audio URL construction:** For auto-translated words, use `/api/audio/pronounce?word={word}&lang={language}&token={jwt}` instead of `/api/audio/{wordId}?token={jwt}`. A new `textAudioUrl(word, lang)` helper should be added alongside the existing `audioUrl(wordId)` in the frontend API module.

### Edge Cases

| Scenario | Handling |
|---|---|
| Word exists in both curated dictionary and TranslationCache | Curated result takes priority (step 2 returns before step 3) |
| Translation service returns empty or nonsensical result | Treat as failure — return `source: null`, do not cache |
| Same word, different reference languages | Each (word, sourceLang, targetLang) triple is cached independently |
| Concurrent requests for the same uncached word | Both hit the translation service; second insert to TranslationCache is a no-op due to unique constraint |
| TTS generation fails for text-based audio | Return 503 with friendly message, same as existing audio endpoint |
| Route ordering: `/api/audio/pronounce` vs `/{word_id}` | `/pronounce` route must be registered before `/{word_id}` in the router |
| Very long "word" (attempted abuse) | Reject with 400 if `word` exceeds 100 characters |
| Word contains only numbers/symbols | Translation service called but likely returns the input unchanged — cached as-is |
| User has no host selected | Default to "marco" (existing fallback in `resolve_host_voice()`) |

### Consequences

**Positive:**
- Single API call for any story word — no sequential frontend logic needed
- Backward-compatible: existing curated lookups work identically; the `source` field is additive
- The text-based audio endpoint completes the coverage gap — every translatable word becomes playable
- Clean separation: curated words use `/api/audio/{wordId}`, on-the-fly words use `/api/audio/pronounce`
- Frontend changes are minimal — one new field check and one new audio URL pattern

**Negative:**
- The lookup endpoint now has side effects (writing to `TranslationCache`) on a GET request — pragmatic but not strictly RESTful. Acceptable because the cache write is idempotent and the client does not need to know about it.
- Two audio endpoint patterns (`/api/audio/{wordId}` and `/api/audio/pronounce`) — adds slight complexity to the audio router
- The text-based audio endpoint accepts arbitrary text, requiring explicit input validation and a new per-user rate limiter
- The `WordLookupResult` schema must be updated in both backend (Pydantic) and frontend (TypeScript) to include the `source` field

**Neutral:**
- ADR-0013's tokenisation and frontend normalisation logic remains unchanged
- ADR-0013's status changes to "Extended by ADR-0027" — the original decision about tokenisation and client-side normalisation still applies
- The `TranslationCache` query adds one indexed database lookup (~0.1 ms) to every dictionary miss — negligible latency impact

## References

- Feature requirements: [on-the-fly-word-lookup.md](../features/on-the-fly-word-lookup.md)
- Related ADRs: [ADR-0007](0007-audio-delivery.md), [ADR-0013](0013-story-word-lookup.md), [ADR-0016](0016-tts-provider-edge-tts.md), [ADR-0025](0025-on-the-fly-translation-provider.md), [ADR-0026](0026-on-the-fly-translation-caching.md)
