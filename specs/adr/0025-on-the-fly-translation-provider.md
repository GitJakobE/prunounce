# ADR-0025: On-the-Fly Translation Provider

- **Status:** Proposed
- **Date:** 2026-04-02
- **Deciders:** Development team
- **Requirements:** REQ-18 (On-the-Fly Word Lookup & Audio)
- **Related:** [ADR-0013](0013-story-word-lookup.md), [ADR-0016](0016-tts-provider-edge-tts.md), [F-OTFLOOKUP](../features/on-the-fly-word-lookup.md)

## Context and Problem Statement

The Story Reading feature requires that clicking any word in a story displays a translation. ADR-0013 established exact-match lookup against the curated dictionary, accepting "Translation not available" for unmatched words as a v1 limitation. In practice, a significant proportion of story words (conjugated verbs, articles, pronouns, declined nouns, common adverbs) have no curated dictionary entry, leaving learners with dead-end clicks that discourage exploration.

REQ-18 requires an external translation source as a fallback when the curated dictionary has no match. The system must translate a single word from the story's target language (Italian, Danish, or English) into the user's selected reference language. The decision here is which translation service or approach to use.

## Decision Drivers

- Must support all six language-pair directions: it↔en, it↔da, en↔da (and reverses)
- Single-word translation quality — the service must handle isolated words and short forms, not just full sentences
- Latency: the combined lookup (dictionary miss + external call) must complete within 3 seconds
- Zero or near-zero cost for v1 — consistent with ADR-0016's zero-API-key philosophy
- No heavy infrastructure — no cloud accounts, billing, or credential provisioning required for local dev
- Results are cached after first lookup, so per-call volume is bounded by vocabulary size, not user traffic
- Must be callable from the Python/FastAPI backend (ADR-0010)
- Acceptable quality for a fallback — users are informed that results are "auto-translated"

## Considered Options

### Option 1: `deep-translator` Python library with Google Translate free endpoint (Chosen)

Use the `deep-translator` package, which wraps multiple free translation APIs. The default backend is Google Translate's free web endpoint (no API key). It supports all required language pairs, returns single-word translations, and is synchronous with low latency (~200–500 ms per call). The library is well-maintained (1.5M+ monthly PyPI downloads) and provides a clean Python API.

**Pros:**
- Zero cost, zero API keys — consistent with existing provider philosophy
- Supports all required language pairs (it, en, da)
- Simple Python API: `GoogleTranslator(source='it', target='en').translate('chiamo')` → `"I call"`
- Low per-call latency (~200–500 ms uncached)
- Fallback providers available within the same library (MyMemory, Linguee) if Google blocks
- Each translation is cached after first call — ongoing request volume to Google is bounded

**Cons:**
- Depends on Google's undocumented free endpoint — may be rate-limited or blocked under heavy use
- Translation quality for isolated conjugated forms may be inconsistent (e.g., "chiamo" might return "I call" or "call" depending on service heuristics)
- No SLA or guarantee of availability
- Not suitable for high-volume production without caching — but caching is already required by REQ-18

### Option 2: Google Cloud Translation API (paid)

Official REST API with documented SLA, consistent quality, and explicit language pair support. Requires a Google Cloud project, API key, and billing account. Charges per character translated.

**Pros:**
- Reliable, documented API with SLA
- Consistent translation quality
- Supports all required language pairs

**Cons:**
- Requires Google Cloud credentials and billing — operational overhead disproportionate for v1
- Cost per character, though minimal given caching
- Adds credential management complexity to dev and deploy workflows
- Contradicts the project's zero-API-key posture for v1

### Option 3: LibreTranslate (self-hosted open-source)

Self-hosted, open-source translation engine using Argos Translate models. No external API dependency.

**Pros:**
- Fully self-hosted — no external service dependency
- Open source, no API keys
- Supports many language pairs

**Cons:**
- Requires running an additional server process (another container/service)
- Model quality for Danish is significantly lower than Google
- Adds operational complexity — downloading models, managing the process
- Higher latency than Google's endpoint for single-word translations

### Option 4: MyMemory Translation API (free tier)

Free translation memory API with 5,000 words/day limit for anonymous use. Higher limits with an API key (free registration).

**Pros:**
- Free tier available with reasonable limits
- Supports all required language pairs
- REST API, easy to call from Python

**Cons:**
- 5,000 words/day anonymous limit may be hit during initial cache warming
- Quality is variable — relies on translation memory contributions
- Less consistent than Google for single-word translations
- Would need `deep-translator` or `requests` anyway

### Option 5: LLM-based translation (e.g., local model or API)

Use a language model to translate words with richer context. Could provide translations, phonetic hints, and even part-of-speech information.

**Pros:**
- Could provide richer output (phonetic hint, part of speech, contextual meaning)
- Quality potentially higher for difficult conjugated forms

**Cons:**
- Significant latency (1–5+ seconds per call) unless using a fast API
- Requires either a paid API (OpenAI, Anthropic) or a local model with substantial resource requirements
- Over-engineered for single-word translation
- Cost and complexity disproportionate to the fallback use case

## Decision Outcome

**Chosen: Option 1 — `deep-translator` with Google Translate free endpoint**

### Rationale

- Aligns with the project's zero-cost, zero-API-key posture established by ADR-0016 (Edge TTS)
- The caching requirement (REQ-18) means Google's free endpoint is only called once per unique (word, source language, target language) triple — volume is bounded by vocabulary, not traffic
- Translation quality for single words is adequate for a clearly-labelled "auto-translated" fallback
- The `deep-translator` library provides built-in fallback to MyMemory if Google rate-limits, adding resilience
- Per-call latency (~200–500 ms) easily fits within the 3-second budget when combined with TTS generation
- If the project later needs higher quality or SLA guarantees, migrating to Google Cloud Translation API (Option 2) requires only changing the translator class — the caching layer and endpoint interface remain identical

### Implementation Details

- **Library:** `deep-translator` (add to `pyproject.toml`)
- **Default backend:** `GoogleTranslator` from `deep-translator`
- **Provider abstraction:** Create a `TranslationProvider` ABC in `app/services/translation.py` with a `GoogleFreeTranslationProvider` implementation — mirrors the `TTSProvider` pattern from ADR-0016
- **Language codes:** Use ISO 639-1 codes (`it`, `en`, `da`) matching the existing `Word.language` field
- **Error handling:** If the translation call fails (network error, rate limit), return `None` — the endpoint returns "Translation temporarily unavailable" and does not cache the failure

### Consequences

**Positive:**
- Zero-cost translation fallback available immediately
- Consistent with the project's provider-abstraction pattern (TTSProvider, TranslationProvider)
- Bounded external API usage due to persistent caching
- Easy migration path to paid APIs if needed

**Negative:**
- Dependency on an undocumented Google endpoint — mitigated by caching and the "auto-translated" label setting user expectations
- Translation quality for some conjugated forms may be imperfect — acceptable given the labelling
- `deep-translator` is an additional Python dependency

**Neutral:**
- This decision covers only the translation provider — the caching strategy and endpoint design are covered in ADR-0026 and ADR-0027 respectively

## References

- Feature requirements: [on-the-fly-word-lookup.md](../features/on-the-fly-word-lookup.md)
- Related ADRs: [ADR-0013](0013-story-word-lookup.md), [ADR-0016](0016-tts-provider-edge-tts.md), [ADR-0024](0024-seeded-audio-generation-strategy.md)
- `deep-translator` PyPI: https://pypi.org/project/deep-translator/
