# Feature Requirements Document — Story Seed Data Cleanup

**Parent PRD:** [prd.md](../prd.md)  
**Related:** [story-reading.md](story-reading.md), [content-review-stories.md](content-review-stories.md)  
**Priority:** P1 (Bug fix — data integrity)

---

## 1. Overview

The story library currently contains duplicate short stories that lack narration audio. These audio-less stories were introduced when an older data source was seeded alongside the primary story seeder, resulting in 6 short stories per language per level instead of the intended 3. Users who encounter a story without audio experience a broken playback flow, undermining trust in the content library. This cleanup removes the orphaned stories and prevents re-seeding.

---

## 2. Problem Statement

- The story library contains **63 short stories** across all languages and levels, but the target (per [story-reading.md](story-reading.md) US-S10) is **3 short stories per difficulty level per language**.
- **36 short stories** (across en, da, it, and es) have **zero narration audio** at any speed. These stories all share a recognisable sequential UUID prefix (`f47ac10b-58cc-...`).
- A second set of **9 Spanish (`es`) stories** exists with no audio and no configured host persona for Spanish, meaning they can never be narrated.
- Two independent seeding paths both insert stories into the same database table, causing duplicates whenever both run.

---

## 3. User Impact

| Scenario | Impact |
|---|---|
| User browses short stories | Sees twice as many stories as intended; half have no audio. |
| User opens an audio-less story and presses Play | Nothing plays — no error message, just silence. Feels broken. |
| User browses Spanish stories (if surfaced) | Entire language has no host persona, no audio, and no pronunciation support. |

---

## 4. Requirements

### 4.1 Remove Stories Without Audio

- All short stories that have **zero associated narration audio files** must be removed from the story library.
- After cleanup, every remaining short story must have at least one audio variant (one host voice at one speed).
- The target count per combination must be **exactly 3 short stories** for every supported language (en, da, it) at every difficulty level (beginner, intermediate, advanced).

### 4.2 Remove Unsupported Language Content

- All stories for languages that do not have a configured host persona (currently: Spanish / `es`) must be removed from the story library.
- If Spanish language support is added in the future, stories should be re-introduced through the standard seeding path with full audio coverage.

### 4.3 Prevent Re-Introduction of Orphaned Stories

- The seeding process must not re-introduce audio-less stories on subsequent runs.
- If multiple data sources feed into the story table, the system must either:
  - Consolidate to a single authoritative source for short stories, **or**
  - Validate that every story inserted has corresponding audio before making it visible to users.

### 4.4 Data Integrity

- Removing a story must also remove any associated records (e.g., audio rows, reading progress, bookmarks) to avoid orphaned references.
- The cleanup must be safe to run on both fresh and existing databases.

---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-1 | After cleanup, querying short stories returns exactly **27 rows**: 3 stories × 3 levels × 3 languages (en, da, it). |
| AC-2 | Every remaining short story has **≥ 1 narration audio** variant. |
| AC-3 | No stories exist for unsupported languages (e.g., `es`) unless a host persona is configured. |
| AC-4 | Running the seed scripts a second time does not re-introduce the removed stories. |
| AC-5 | The story library UI shows exactly 3 short stories per level per language, all playable. |

---

## 6. Out of Scope

- Adding new stories to replace the removed ones.
- Generating audio for the removed stories retroactively (they were never intended to co-exist with the primary set).
- Spanish language support — that is a separate feature if/when a Spanish host persona is added.
- Changes to medium or long stories (this FRD focuses on the short-story duplication issue; if the same pattern exists for other lengths, a follow-up should address it).

---

## 7. Affected Stories (Reference)

The following 36 stories (all with zero audio) should be removed:

**Italian (it):**
`al-caffe`, `ciao-come-stai`, `al-mercato`, `una-giornata-a-roma`, `la-cena-di-famiglia`, `fare-la-spesa`, `la-storia-della-pasta`, `il-carnevale-di-venezia`, `la-dolce-vita-italiana`

**Danish (da):**
`god-morgen`, `pa-bageren`, `i-parken`, `hygge-derhjemme`, `en-tur-til-museet`, `dansk-cykelkultur`, `kobenhavn-og-vandet`, `det-nordiske-kokken`, `det-danske-sprog`

**English (en):**
`morning-routine`, `at-the-coffee-shop`, `in-the-park`, `planning-a-trip`, `a-job-interview`, `cooking-at-home`, `city-and-countryside`, `history-of-english`, `digital-age`

**Spanish (es) — entire language:**
`en-el-cafe`, `hola-que-tal`, `en-el-mercado`, `un-dia-en-madrid`, `la-cena-familiar`, `de-compras`, `la-historia-de-las-tapas`, `el-camino-de-santiago`, `la-vida-espanola`
