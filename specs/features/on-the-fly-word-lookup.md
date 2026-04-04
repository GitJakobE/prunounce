# Feature Requirements Document — On-the-Fly Word Lookup & Audio Generation

**Parent PRD:** [prd.md](../prd.md)  
**Feature ID:** F-OTFLOOKUP  
**Related:** [story-reading.md](story-reading.md), [audio-pronunciation.md](audio-pronunciation.md), [word-dictionary.md](word-dictionary.md), ADR-0013, ADR-0024  
**Priority:** P1 (High — addresses major content gap in story reading)

---

## 1. Overview

Stories naturally contain many words that are not in the curated dictionary — conjugated verbs, declined nouns, articles, pronouns, adverbs, and other inflected or grammatical forms. Currently, clicking any of these words in the story reading view shows "Translation not available" with no audio, which breaks the learning flow and frustrates users.

This feature closes that gap by introducing **on-the-fly translation lookup** and **on-the-fly audio generation** for any word in a story that is not already in the curated dictionary or audio cache. The result is that every clickable word in a story produces a useful translation and playable pronunciation, whether or not it was pre-seeded.

---

## 2. Problem Statement

- A significant proportion of words in stories are not exact matches for curated dictionary entries (e.g., "chiamo" vs. dictionary entry "chiamare", or common words like "il", "è", "molto" that were never seeded).
- Users clicking these words see a dead end ("Translation not available"), which undermines confidence in the product and discourages exploration.
- Audio is only available for words that were pre-generated or exist in the dictionary, leaving many story words silent.
- The current experience trains users to stop clicking words — the opposite of the intended learning behaviour.

---

## 3. User Stories

| ID | Story | Acceptance Criteria |
|---|---|---|
| US-OTF1 | As a learner reading a story, I want to click any word and see a translation, even if the word is not in the curated dictionary. | Clicking a word that is not in the dictionary still displays a translation in my reference language within 3 seconds. |
| US-OTF2 | As a learner reading a story, I want to hear the pronunciation of any word I click, even if audio was not pre-generated. | Clicking the play button for an uncached word generates and plays audio within 3 seconds on first click; subsequent clicks play instantly from cache. |
| US-OTF3 | As a learner, I want to know whether a translation came from the curated dictionary or was generated on the fly, so I can gauge its reliability. | The translation panel shows a subtle indicator (e.g., "auto-translated") when the result did not come from the curated dictionary. |
| US-OTF4 | As a learner, I want on-the-fly lookups to be fast on repeat clicks, so I don't wait every time. | Once a word has been looked up or its audio generated, the result is cached and served instantly on subsequent interactions. |
| US-OTF5 | As a learner, I want the experience to degrade gracefully if the translation or audio service is temporarily unavailable. | If on-the-fly lookup fails, the panel shows a clear, friendly message ("Translation temporarily unavailable — please try again shortly") rather than a cryptic error. |

---

## 4. Functional Requirements

### 4.1 Translation Lookup Cascade

When a user clicks a word in the story reading view, the system must attempt to resolve a translation using the following cascade:

1. **Local session cache** — If the word was already looked up during this reading session, return the cached result instantly (no network call).
2. **Curated dictionary** — Look up the word (after normalisation) in the existing curated dictionary. If found, return the stored translation and phonetic hint. *(This is the existing behaviour.)*
3. **On-the-fly translation** — If the dictionary has no match, the system must request a translation from an external translation source. The translation must be from the story's target language into the user's selected reference language.

The cascade must be invisible to the user — they click a word and get a result. The only visible difference is a small indicator showing whether the result is curated or auto-translated.

### 4.2 On-the-Fly Translation Behaviour

- The system must translate the clicked word from the target language to the user's reference language.
- The translation should be contextually appropriate for a single word or short phrase (not a full-sentence translation).
- A phonetic hint is **not required** for on-the-fly translations (it may be omitted or marked as unavailable). If the service can provide one, it should be displayed.
- The translated result must be cached on the backend so that subsequent lookups of the same word (by any user, for the same language pair) do not call the external service again.
- The translation panel must display the result within **3 seconds** of the user's click for an uncached word.

### 4.3 On-the-Fly Audio Generation

- If a user clicks the play button for a word that does not have pre-generated audio in the cache, the system must generate audio on-the-fly using the existing TTS provider (Microsoft Edge TTS).
- Audio must be generated using the user's **currently selected host's voice** only — not for all host voices.
- The generated audio file must be stored in the existing audio cache so that:
  - The same user replaying the word hears it instantly.
  - Any other user with the same host voice also gets the cached version.
- First-play latency for an uncached word must not exceed **3 seconds**.
- Subsequent plays of the same word+host combination must play within **1 second** (from cache).

### 4.4 Caching Requirements

- **Translation cache:** On-the-fly translations must be persisted on the backend, keyed by (word, target language, reference language). Once generated, a translation is reused across all users and sessions.
- **Audio cache:** On-the-fly audio must be stored in the same cache infrastructure used by pre-generated audio, keyed by (word, host voice). Once generated, audio is reused across all users.
- **Session cache:** The frontend must maintain a local in-memory cache of all lookup results for the duration of a story reading session, avoiding redundant network calls for repeated clicks on the same word.
- Both caches must be additive — on-the-fly results do not overwrite or interfere with curated dictionary entries.

### 4.5 Source Indicator

- The translation panel must indicate whether a result came from the **curated dictionary** or was **auto-translated on the fly**.
- Curated results: no special indicator (current default appearance).
- Auto-translated results: a small, non-intrusive label such as "auto-translated" displayed below the translation text.
- This indicator helps users understand that auto-translated results may be less precise than curated entries, without discouraging use.

### 4.6 Error Handling

- If the on-the-fly translation service is unavailable or returns an error, the panel must display: **"Translation temporarily unavailable — please try again shortly."**
- If on-the-fly audio generation fails, the play button must show a brief error state and the user should be able to retry.
- Failures in on-the-fly services must not affect the display or playback of curated dictionary words.
- Transient failures should not be cached — a failed lookup should be retryable on the next click.

### 4.7 Scope

- **Primary scope:** Story reading view — clicking words in story text.
- **Reusable:** The on-the-fly lookup endpoint should be designed so it can be reused by other features in the future (e.g., word search, user-contributed word preview), but those integrations are not part of this feature's scope.
- **Out of scope for this feature:**
  - Morphological analysis or lemmatisation (the system translates the word as-is; "chiamo" is translated as "chiamo", not resolved to "chiamare" first)
  - Bulk pre-translation of all story words at seed time
  - Admin review or curation workflow for auto-translated entries

---

## 5. Edge Cases

| Scenario | Expected Behaviour |
|---|---|
| Word exists in curated dictionary | Dictionary result returned; no on-the-fly call made. Panel shows curated result with no "auto-translated" label. |
| Word not in dictionary, translation service succeeds | Auto-translated result displayed with "auto-translated" indicator. Result cached for future lookups. |
| Word not in dictionary, translation service fails | Panel shows "Translation temporarily unavailable — please try again shortly." Result is not cached. |
| Word not in dictionary, audio not cached, TTS succeeds | Audio generated, played, and cached. Subsequent plays are instant. |
| Word not in dictionary, audio not cached, TTS fails | Play button shows error state. User can retry. No broken audio cached. |
| User switches host (different voice) mid-story | Audio cache is per host voice. A new host voice triggers fresh audio generation for uncached words. Translation cache is unaffected. |
| Same word clicked by different users with different reference languages | Translation cached per (word, target language, reference language). Each language pair is independently cached. |
| Proper nouns (character names, place names) | Translated as-is by the external service — likely returned unchanged, which is correct behaviour. |
| Numbers and symbols | May return a literal translation or "Translation not available" — acceptable. |

---

## 6. Acceptance Criteria

- [ ] Clicking any word in a story returns a translation — either from the curated dictionary or via on-the-fly lookup — within 3 seconds.
- [ ] On-the-fly translations are visually distinguished from curated translations with an "auto-translated" indicator.
- [ ] On-the-fly translations are cached on the backend; a second lookup of the same word (same language pair) does not call the external service.
- [ ] Clicking play on a word with no pre-generated audio triggers on-the-fly TTS generation and playback within 3 seconds.
- [ ] On-the-fly generated audio is cached in the existing audio cache and replays within 1 second.
- [ ] If the translation or audio service is unavailable, a friendly error message is shown and the user can retry.
- [ ] Curated dictionary lookups continue to work exactly as before — no regression.
- [ ] The frontend caches all lookup results in-session to avoid redundant API calls.
- [ ] The feature works across all three target languages (Italian, Danish, English) and all reference language combinations.

---

## 7. Dependencies

- Existing dictionary lookup endpoint (ADR-0013)
- Existing audio cache and TTS generation infrastructure (ADR-0007, ADR-0016, ADR-0024)
- An external translation capability for on-the-fly lookups (selection of specific service is a technical decision for the dev team)

---

## 8. Success Metrics

| Metric | Target |
|---|---|
| Percentage of story word clicks that return a translation (vs. "not available") | ≥ 95% |
| Percentage of story word clicks that have playable audio | ≥ 95% |
| Average latency for uncached on-the-fly lookup (translation + audio) | ≤ 3 seconds |
| Average latency for cached lookups | ≤ 500 ms |
| User engagement: words clicked per story session | Increase by ≥ 30% vs. current baseline |
