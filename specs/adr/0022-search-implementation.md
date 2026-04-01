# ADR-0022: Search Implementation — In-Memory Normalize-and-Rank

- **Status:** Accepted
- **Date:** 2026-03-29
- **Deciders:** Development team
- **Requirements:** F-SEARCH (Word Search & Lookup), REQ-5

## Context and Problem Statement

The Word Search FRD (F-SEARCH) requires a search experience that is case-insensitive, tolerant of missing diacritical marks (e.g., "perche" matches "perché", "hojre" matches "højre"), works across both target and reference languages, and returns ranked results within 500 ms. The team needs to decide how to implement this given the SQLite database (ADR-0003), the Python/FastAPI backend (ADR-0010), and the expected dataset size (~250 words per language at launch, growing with user contributions).

## Decision Drivers

- Diacritical-mark tolerance is critical for Danish (æ, ø, å) and Italian (à, è, é, ì, ò, ù) learners who may not know how to type special characters
- The dataset is small: ~750 words at launch across three languages, growing to a few thousand with contributions
- Search must work in both the target language and the user's reference language simultaneously
- Results must be ranked: exact match → prefix match → substring match
- SQLite has FTS5 support, but diacritical-mark normalization requires custom tokenizers
- The current implementation already uses in-memory normalize-and-rank and works correctly

## Considered Options

### Option 1: In-Memory Normalize-and-Rank (Chosen)

Load all words for the user's target language from the database, apply a Python normalization function that strips diacritical marks and lowercases, then score each word against the normalized query (exact=3, prefix=2, contains=1). Return results sorted by score.

### Option 2: SQLite FTS5 with Custom Tokenizer

Create an FTS5 virtual table with a custom tokenizer that normalizes diacritical marks. FTS5 handles ranking natively. However, SQLite's custom tokenizer API requires C extensions or the `unicode61` tokenizer with `remove_diacritics=2`, which may not handle all Danish/Italian characters correctly.

### Option 3: SQLite LIKE with Application-Side Normalization Column

Add a `word_normalized` column to the Word table (pre-computed, stripped of diacritics). Search using `LIKE '%term%'` on the normalized column. Simpler than FTS5 but requires maintaining the normalized column on insert/update and doesn't provide natural ranking.

### Option 4: External Search Service (Meilisearch / Typesense)

Deploy a lightweight search engine alongside the app. Provides typo tolerance, faceted search, and excellent ranking out of the box. However, this adds operational complexity (another service to deploy, keep in sync) that is disproportionate for a ~750-word dataset.

## Decision Outcome

**Chosen: Option 1 — In-Memory Normalize-and-Rank**

For the expected dataset size, loading all words into memory and ranking in Python is the simplest approach that meets all requirements. The normalization function handles diacritical marks explicitly, and the three-tier ranking (exact → prefix → contains) satisfies the FRD's relevance requirement.

### Implementation Details

- **Normalization function:** A character mapping that converts accented characters to their ASCII base (à→a, ø→o, å→a, etc.), applied to both the search query and each word/translation
- **Search scope:** All words where `language == target_lang`, checked against both the target-language word and the reference-language translation
- **Ranking tiers:** Score 3 (exact match) → Score 2 (prefix match) → Score 1 (substring match)
- **Performance:** With ~250 words per language, the entire search completes in < 10 ms — well within the 500 ms budget

### Scaling Threshold

This approach is appropriate for datasets up to ~10,000 words per language. If the dictionary grows beyond that (unlikely given the product scope), the team should revisit and consider Option 3 (normalized column with indexed LIKE) or Option 4 (external search).

### Consequences

**Positive:**
- Zero additional infrastructure — no new services, no FTS5 setup
- Full control over diacritical-mark normalization for Danish and Italian edge cases
- Ranking logic is transparent and easy to adjust
- Already implemented and tested in the current codebase

**Negative:**
- Loads all words for the target language on every search request (mitigated by small dataset and SQLAlchemy's query caching)
- Normalization function must be maintained manually when new languages/characters are added
- No fuzzy/typo tolerance — only diacritical-mark stripping (the FRD does not require fuzzy matching)

**Neutral:**
- If a future ADR adds a new language with a non-Latin script, this approach would need significant extension
- The normalization map is deterministic and easily unit-testable
