# ADR-0026: On-the-Fly Translation & Audio Caching Strategy

- **Status:** Proposed
- **Date:** 2026-04-02
- **Deciders:** Development team
- **Requirements:** REQ-18 (On-the-Fly Word Lookup & Audio)
- **Related:** [ADR-0007](0007-audio-delivery.md), [ADR-0024](0024-seeded-audio-generation-strategy.md), [ADR-0025](0025-on-the-fly-translation-provider.md), [F-OTFLOOKUP](../features/on-the-fly-word-lookup.md)

## Context and Problem Statement

REQ-18 requires that on-the-fly translation and audio results are cached so that:
1. A second lookup of the same word does not call the external translation service again.
2. A second play of the same word+host does not trigger TTS generation again.
3. Any user benefits from translations and audio previously generated for other users.

The system already has two caching mechanisms: the `Word` table in SQLite for curated dictionary entries, and the `audio-cache/` directory for generated audio files (ADR-0007). The decision is how to persist on-the-fly translation results — whether to reuse the existing `Word` table, introduce a new table, or use a separate cache store — and how on-the-fly audio integrates with the existing file cache.

## Decision Drivers

- On-the-fly translations must be persistent across server restarts and shared across all users
- On-the-fly translations must not pollute or be confused with curated dictionary entries
- Audio caching for on-the-fly words should reuse the existing file-based cache (ADR-0007) to avoid a second delivery mechanism
- Lookup latency for cached results must be under 1 second
- The caching strategy must be additive — it must not affect existing curated dictionary lookup behaviour
- Schema changes must be manageable with the existing Alembic migration workflow
- The frontend also needs a session-level cache to avoid redundant network calls

## Considered Options

### Option 1: New `TranslationCache` table in SQLite (Chosen)

Add a dedicated `TranslationCache` table to store on-the-fly translation results separately from the curated `Word` table. Columns: `word`, `source_language`, `target_language`, `translation`, `created_at`. Unique constraint on `(word, source_language, target_language)`. Audio continues to use the existing `audio-cache/` filesystem cache keyed by `{sanitized_word}_{hostId}.mp3`.

### Option 2: Add on-the-fly translations as rows in the existing `Word` table

Insert auto-translated words into the `Word` table with `source = 'auto-translated'`. This reuses existing query paths and the `wordId`-based audio endpoint.

**Pros:**
- No new table; reuses existing query paths and audio endpoint
- `wordId` available for audio URL construction

**Cons:**
- Pollutes the curated dictionary — auto-translated entries would appear in category listings, search results, and word counts unless every query adds a `WHERE source != 'auto-translated'` filter
- Missing required fields: `phonetic_hint`, `difficulty`, `category` — would need nullable columns or dummy values
- Conflates two fundamentally different data types: curated, reviewed entries and auto-generated fallbacks
- Makes the `Word` table's unique constraint (`word` + `language`) problematic — a curated "ciao" and an auto-translated "ciao" would conflict

### Option 3: In-memory cache only (e.g., Python dict or Redis)

Cache translations in an in-process dictionary or external Redis store. No database persistence.

**Pros:**
- Fastest possible lookup for cached results
- No schema changes

**Cons:**
- In-process cache is lost on server restart — all translations regenerated
- Redis adds infrastructure complexity (ADR-0024 rejected queue infrastructure for v1)
- Not shared across multiple server instances without Redis
- Unbounded memory growth without eviction policy

### Option 4: Filesystem JSON cache

Store translations as JSON files on disk, keyed by word and language pair.

**Pros:**
- Simple, no database changes
- Persistent across restarts
- Matches the audio cache's filesystem approach

**Cons:**
- No indexing — lookup requires reading a file per request or loading all into memory
- Harder to query, report on, or clean up than a database table
- Doesn't benefit from SQLite's ACID guarantees or indexed lookups

## Decision Outcome

**Chosen: Option 1 — New `TranslationCache` table in SQLite**

### Rationale

- Clean separation between curated dictionary entries and auto-translated fallbacks — no risk of polluting word lists, search results, or progress tracking
- SQLite provides indexed, ACID-compliant storage with sub-millisecond lookups on the unique constraint
- Aligns with the existing Alembic migration workflow — adding a table is straightforward
- Persistent across restarts and shared across all request handlers in the same process
- The frontend session cache (in-memory `Map`) provides the first layer; the database provides the persistent shared layer

### Schema

```sql
CREATE TABLE TranslationCache (
    id          TEXT PRIMARY KEY,  -- UUID generated by Python uuid4(), consistent with existing models
    word        TEXT NOT NULL,
    sourceLang  TEXT NOT NULL,   -- language of the word (app's "target language", e.g., 'it' for Italian stories)
    targetLang  TEXT NOT NULL,   -- language of the translation (app's "reference language", e.g., 'en')
    translation TEXT NOT NULL,
    createdAt   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(word, sourceLang, targetLang)
);
CREATE INDEX idx_translation_cache_lookup ON TranslationCache(word, sourceLang, targetLang);
```

**Naming note:** In translation terminology, `sourceLang` is the language being translated *from* and `targetLang` is the language being translated *to*. This is the **opposite** of the app's user-facing naming (where "target language" = language being learned and "reference language" = user's native language). The column names use translation-standard nomenclature to avoid confusion within the translation service layer. A comment in the model should clarify the mapping.

### Audio Caching

On-the-fly audio reuses the existing `audio-cache/` filesystem cache from ADR-0007:
- **Cache key:** `{sanitized_word}_{hostId}.mp3` — identical to curated word audio
- **Generation:** The existing `get_audio_path()` function in `app/services/tts.py` already generates-on-miss and caches. On-the-fly audio calls the same function with the clicked word text and the user's host voice.
- **No separate audio cache needed** — the file cache is keyed by word text, not by word ID. An on-the-fly word ("chiamo") and a curated word ("chiamare") naturally get separate cache files.

### Frontend Session Cache

- The frontend maintains a `Map<string, LookupResult>` for the duration of each story reading session (as specified in ADR-0013).
- This map now caches both curated and on-the-fly results.
- Clicking the same word twice never triggers a second API call, regardless of the result source.

### Cache Lifecycle

- **Translation cache entries are permanent** — once a translation is cached, it persists indefinitely. Auto-translations are unlikely to change.
- **No TTL or eviction** — the cache grows proportionally to unique words encountered across all stories, bounded by story vocabulary size (estimated <5,000 unique entries across all languages).
- **No cache invalidation needed** for v1. If a curated dictionary entry is later added for a word that has a cached auto-translation, the lookup cascade (ADR-0027) checks the curated dictionary first, so the auto-translation is naturally shadowed.
- **Audio cache entries follow the same lifecycle as ADR-0024** — persistent, no expiry.

### Consequences

**Positive:**
- Clean separation: auto-translations never appear in dictionary browsing, search, or progress tracking
- Sub-millisecond cached lookups via SQLite index
- Persistent across restarts — bounded external API calls over the lifetime of the deployment
- Reuses existing audio cache infrastructure — no new file-serving mechanism needed
- Natural shadowing: adding a curated entry for a word automatically takes priority over the cached auto-translation

**Negative:**
- New database table requires an Alembic migration
- On-the-fly words do not have a `wordId` — the audio endpoint needs an alternative path that accepts word text instead of word ID (addressed in ADR-0027: `GET /api/audio/pronounce`)
- Storage grows with vocabulary diversity, though bounded and small

**Neutral:**
- The frontend session cache implementation is unchanged from ADR-0013 — it simply caches a broader set of results
- Failed translation attempts are not cached — the external service is retried on next click

## References

- Feature requirements: [on-the-fly-word-lookup.md](../features/on-the-fly-word-lookup.md)
- Related ADRs: [ADR-0007](0007-audio-delivery.md), [ADR-0013](0013-story-word-lookup.md), [ADR-0024](0024-seeded-audio-generation-strategy.md), [ADR-0025](0025-on-the-fly-translation-provider.md)
