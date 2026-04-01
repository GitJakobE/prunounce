# ADR-0013: Story Word Tokenisation & Dictionary Lookup

- **Status:** Proposed
- **Date:** 2026-03-29
- **Deciders:** Development team
- **Requirements:** REQ-14 (Story Reading), REQ-2 (Word dictionary), REQ-5 (Word search)

## Context and Problem Statement

The Story Reading feature requires every word in a story to be individually clickable. When a user clicks a word, the translation panel must show the word's reference-language translation, a phonetic hint, and a play button. This requires two capabilities:

1. **Tokenisation** — Breaking the raw story text into discrete, clickable word tokens while preserving punctuation and formatting for display.
2. **Dictionary lookup** — Matching a clicked token against the word dictionary to retrieve its translation and phonetic hint.

The challenge is that story text contains natural language: punctuation attached to words ("Buongiorno!"), conjugated verb forms ("chiamo" vs. dictionary entry "chiamare"), capitalised sentence starts, and words that may not exist in the curated dictionary at all. The lookup strategy must be practical and predictable without requiring a full morphological analyser.

## Decision Drivers

- Every visible word in the story must be a clickable element
- Punctuation must be displayed but not interfere with dictionary lookups
- The dictionary contains base forms (~250+ words per language); stories naturally use conjugated and declined forms
- Lookup latency must be low (user expects instant translation after clicking)
- The approach must work across Italian, Danish, and English without language-specific morphology rules
- Simplicity: avoid adding NLP dependencies for v1 — the FRD accepts "Translation not available" for unmatched words

## Considered Options

### Option 1: Frontend tokenisation with backend exact-match lookup after normalisation (Chosen)

The frontend splits the story body into tokens using whitespace and punctuation boundaries. When a word is clicked, the frontend strips surrounding punctuation and sends the normalised form to a backend lookup endpoint. The backend performs a case-insensitive, diacritical-tolerant exact match against the `Word` table. If no match is found, the panel shows "Translation not available."

### Option 2: Backend tokenisation with pre-computed word links

The backend pre-processes each story's text, tokenises it, matches tokens against the dictionary, and returns the story as an array of `{ text, wordId | null }` objects. The frontend renders this pre-linked structure. This provides perfect consistency but tightly couples stories to the dictionary — any dictionary change requires re-processing all stories, and the response payload is significantly larger.

### Option 3: Full morphological analysis with lemmatisation

Use an NLP library (e.g., spaCy for Python) to lemmatise clicked words before lookup. "chiamo" → "chiamare", "mangiato" → "mangiare". This maximises match rates but adds a significant dependency (~100+ MB model per language), increases backend complexity, and introduces latency for the lemmatisation step.

### Option 4: Fuzzy/partial matching (LIKE queries)

Use SQL `LIKE '%word%'` or trigram similarity to find approximate matches. This could match conjugated forms but produces false positives (e.g., "pan" matching "pane" and "panino") and unpredictable results that confuse users.

## Decision Outcome

**Chosen: Option 1 — Frontend tokenisation with backend exact-match lookup after normalisation**

### Tokenisation (Frontend)

The frontend is responsible for splitting the story body into renderable, clickable tokens:

1. **Split on whitespace** — Each whitespace-separated segment is a raw token.
2. **Separate punctuation** — Leading and trailing punctuation (`.`, `,`, `!`, `?`, `;`, `:`, `"`, `'`, `(`, `)`, `—`, `…`) is separated from the word core but kept as adjacent non-clickable text elements.
3. **Preserve display** — The rendered output maintains the original text appearance including punctuation and capitalisation.
4. **Clickable span** — Each word core (without surrounding punctuation) is wrapped in a clickable `<span>` element.

**Example:**
```
Input:  "Buongiorno! Mi chiamo Marco."
Tokens: [("Buongiorno", "!"), (" "), ("Mi", ""), (" "), ("chiamo", ""), (" "), ("Marco", ".")]
Render: <span class="word">Buongiorno</span>! <span class="word">Mi</span> <span class="word">chiamo</span> <span class="word">Marco</span>.
```

### Lookup (Backend)

When a word is clicked, the frontend sends the cleaned word to the backend:

**Endpoint:** `GET /api/dictionary/lookup?word={word}&lang={language}`

**Normalisation steps (backend):**
1. Trim whitespace
2. Convert to lowercase
3. Strip diacritical marks for comparison (e.g., "café" matches "cafe") — uses Unicode NFKD decomposition; the original accented form in the database is still returned in the response
4. Perform exact match against the `Word.word` column (also lowercased and diacritical-stripped) where `Word.language` matches the target language

**Response (match found):**
```json
{
  "word": "buongiorno",
  "translation": "good morning",
  "phoneticHint": "bwon-JOHR-noh",
  "wordId": "uuid-here"
}
```

The `wordId` is included so the frontend can construct the audio play URL (`/api/audio/{wordId}?token=...`) using the existing audio delivery mechanism (ADR-0007).

**Response (no match):**
```json
{
  "word": "chiamo",
  "translation": null,
  "phoneticHint": null,
  "wordId": null
}
```

The frontend displays "Translation not available" in the panel.

### Caching & Performance

- The frontend caches lookup results in a local map (`Map<string, LookupResult>`) for the duration of the story reading session. Clicking the same word twice does not trigger a second API call.
- The backend query uses indexed columns (`Word.word` + `Word.language` via the existing unique constraint) for sub-millisecond lookup.
- No debouncing is needed — lookups are triggered by discrete click events, not continuous input.

### Edge Cases

| Scenario | Handling |
|---|---|
| Punctuation attached to word | Frontend strips punctuation before sending to backend |
| Capitalised word (sentence start) | Backend normalises to lowercase for comparison |
| Diacritical marks (è, ø, å) | Backend strips diacriticals for comparison; returns the original accented form |
| Hyphenated word ("well-known") | Lookup as whole first; if no match, do not attempt split (v1 simplicity) |
| Contractions ("l'amore" in Italian) | Lookup as whole first; if no match, split on apostrophe and look up each part separately |
| Number tokens ("42", "3°") | No dictionary lookup; panel shows "Translation not available" |
| Word not in dictionary | Panel shows "Translation not available" with the clicked word displayed |

### Consequences

**Positive:**
- Simple, predictable behaviour — users understand that exact dictionary words are translatable
- No NLP dependencies — zero additional backend libraries or language models
- Low latency — single indexed database query per click, with frontend caching
- Reuses the existing `Word` table and audio delivery infrastructure
- Frontend tokenisation is a pure string operation with no server round-trip
- The lookup endpoint is generic and reusable by other features

**Negative:**
- Conjugated verb forms and declined nouns will show "Translation not available" unless the base form happens to match — this is an accepted v1 limitation
- Match rate depends on how well story text aligns with dictionary entries — stories should be authored with awareness of the available dictionary
- Italian contractions (e.g., "l'acqua") require special apostrophe-splitting logic

**Neutral:**
- A future enhancement could add a `StoryWordHint` table that maps specific non-dictionary tokens in a story to their base-form dictionary entry, authored alongside the story seed data — this would improve match rates without adding NLP
- Lemmatisation (Option 3) remains a viable upgrade path if match rates prove too low after launch — the lookup endpoint's interface would not change
