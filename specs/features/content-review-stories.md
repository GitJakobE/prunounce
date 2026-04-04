# Feature Requirements Document — Content Review & Validation for Stories

**Parent PRD:** [prd.md](../prd.md)  
**Related:** [story-reading.md](story-reading.md), REQ-14, REQ-16

---

## 1. Overview

As the story library grows with both seeded and user-contributed content, editorial validation ensures that all stories meet quality standards and fulfil the variety requirements laid out in Story Reading (F-STORY). This document defines the mandatory checks and editorial checklists that content authors, reviewers, and QA must apply before stories are published.

---

## 2. Problem Statement

- Stories can be submitted or seeded without clear validation of narrative variety, scope differentiation, and content quality.
- Without editorial oversight, the story library risks becoming repetitive (e.g., all beginners' stories are café orders, all intermediates are doctor visits).
- Story difficulty tiers must be materially different, not just longer versions of the same template.
- Content gaps (missing translations, poor grammar, inadequate word coverage) can slip through if not checked systematically.

---

## 3. Story Variety & Differentiation Requirements

### 3.1 Setup Type Diversity

Each language's story catalogue must include varied narrative patterns **within each difficulty tier**:

- **Arrival/Transaction Setup** – Entering a location and conducting a transaction (café, shop, market, train station).
- **Dialogue-Driven Setup** – A conversation between two or more characters with back-and-forth exchanges but no formal transaction (neighbours meeting, friends discussing plans, family chat).
- **Problem-Solving Setup** – A character encounters a challenge and works toward resolution (broken appliance, lost item, health concern, scheduling conflict).
- **Event/Preparation Setup** – Planning or describing an upcoming or past event (holiday packing, party preparation, trip summary, anniversary dinner).
- **Narrative/Descriptive Setup** – A first-person or third-person account of a memory, observation, or folk tale (no dialogue structure, or dialogue embedded within narration).
- **Discovery/Unexpected Setup** – A character discovers something surprising or new (unusual item, new place, surprising news).

### 3.2 Difficulty Tier Scope Requirements

**Beginner Stories:**
- One clear scenario or situation that can be described in a single sentence (e.g., "A woman orders coffee and a pastry in an Italian café").
- Limited cast: maximum 2 regular speakers (e.g., Customer and Barista).
- One primary objective or exchange: the scenario has a single "task" or interaction (order → pay → leave).
- Tightly constrained vocabulary load: ~80–120 unique words, drawn from the Beginner word dictionary.
- No complication, plot twist, or narrative development beyond the transaction.
- Duration: 100–150 words.

**Intermediate Stories:**
- A scenario with at least one meaningful development, complication, or plot point:
  - A small misunderstanding that must be cleared up, OR
  - A choice the character must make, OR
  - A secondary event or detail that extends the primary scenario (e.g., customer asks about opening hours after ordering), OR
  - A short sequence of related events (e.g., visiting a museum, ordering, then eating).
- Can include 2–3 speakers or a brief ensemble.
- Vocabulary load: ~150–200 unique words, drawn mostly from Beginner and Intermediate dictionaries with a few new terms.
- Duration: 200–300 words.

**Advanced Stories:**
- A broader narrative arc with multiple substantive beats:
  - Several distinct phases (e.g., arriving, explaining a problem, negotiating terms, concluding), OR
  - A character's emotional or intellectual journey (e.g., going from uncertain to confident, confused to understanding), OR
  - Richer descriptive language or reflection woven through dialogue or narration.
- Can feature 3–4 named speakers or a richer ensemble.
- Vocabulary load: ~300–400 unique words, including Beginner, Intermediate, and Advanced terms.
- Cannot be compressed into a beginner or intermediate story by removing details or downplaying development — the story inherently requires the additional scope.
- Duration: 400–600 words.

### 3.3 Setup Type Distribution at Launch

At launch, within each language and each difficulty tier, the minimum set of 3 stories must NOT cluster around a single setup type. Acceptable distributions include:

| Setup Type A | Setup Type B | Setup Type C | Notes |
|---|---|---|---|
| Arrival/Transaction | Dialogue-Driven | Problem-Solving | Balanced across three distinct types. |
| Event/Preparation | Narrative/Descriptive | Discovery/Unexpected | Narrative and reflective pieces included. |
| Arrival/Transaction | Problem-Solving | Dialogue-Driven | Common setups paired with variety. |

**Unacceptable** distributions:
- All 3 stories are Arrival/Transaction (e.g., café, market, train station all follow the same "arrive → conduct business → leave" pattern).
- All 3 stories are dialogue-only without narrative context or scene-setting.
- Stories within the same tier differ only superficially (e.g., "Order coffee at café A" vs. "Order tea at café B").

---

## 4. Content Validation Checklist

### 4.1 Pre-Submission Editorial Review

Before a story is submitted to the content seeding process or approved for user contributions, the author must validate:

- [ ] **Scope & Difficulty:** Does the story fit the difficulty tier's definition (Beginner: single objective; Intermediate: one development; Advanced: multiple beats)?
- [ ] **Setup Type:** Is the story's opening premise distinct from other stories in the same language-difficulty group?
- [ ] **Narrative Structure:** Does the story have a clear beginning, middle, and end? Is there a reason for the reader to keep going?
- [ ] **Word Choices:** Are 85–95% of words in the story present in the target language's dictionary? List any new or uncommon words introduced.
- [ ] **Grammar & Mechanics:** Has the text been checked for spelling, grammatical correctness, and punctuation?
- [ ] **Speaker Consistency:** If dialogue, are speaker names and labels consistent throughout? Are there no more than 4 speakers?
- [ ] **Target Language Authenticity:** Does the dialogue sound natural and idiomatic in the target language? Can a native speaker confirm naturalness?
- [ ] **Translation Completeness:** Are descriptions provided in all three reference languages (English, Danish, Italian)?
- [ ] **Audio Compatibility:** If dialogue-formatted, do speaker turns represent a reasonable amount of audio per character? Are there no excessively long monologues?

### 4.2 Launch Catalogue Validation

Before v1.0 launch, the full set of 27 stories (9 per language, 3 per difficulty) must be reviewed for overall catalogue health:

- [ ] **No Duplicates:** No two stories share substantially the same opening, setting, and progression (e.g., "Meet a friend at a café" appears in Italian Beginner and Italian Intermediate with minor changes).
- [ ] **Setup Type Coverage:** Within each language-difficulty group, at least 2–3 distinct setup types are represented across the 3 stories.
- [ ] **Difficulty Differentiation:** A reader can clearly perceive scope and complexity differences between Beginner, Intermediate, and Advanced stories in the same language.
- [ ] **Dictionary Coverage:** For each language at each difficulty level, the combined vocabulary of the 3 stories includes the target coverage from the word catalogue (e.g., at least 80% of required thematic categories are represented).
- [ ] **Narration Quality:** Each story is readable aloud in under 5 minutes (Beginner ~1–2 min, Intermediate ~2–3 min, Advanced ~3–5 min) with clear natural pacing.
- [ ] **Cultural Appropriateness:** Stories reflect realistic, contemporary scenarios in each language's target regions; no outdated or stereotypical content.

### 4.3 Acceptance Criteria for Publishing

A story is approved for publication when:

- [ ] All items in § 4.1 (Pre-Submission) are marked complete.
- [ ] The story's setup type has been documented and is distinct from other stories in the same language-difficulty tier.
- [ ] If part of launch catalogue, the story has been cross-checked against § 4.2 (Launch Validation) criteria.
- [ ] A native speaker or fluent editor has reviewed the story for naturalness and cultural fit.
- [ ] If applicable, audio has been generated in all 5 speeds and validated for quality.

---

## 5. Content Metadata & Editorial Notes

Each seeded story should include editorial metadata to support content review and help prevent future duplicates:

```
{
  "slug": "it-intermediate-museum-day",
  "language": "it",
  "difficulty": "intermediate",
  "length": "short",                           # Not used currently, but reserved for future
  "title": "Una giornata al museo",
  "setup_type": "Event/Preparation",           # NEW: Editorial metadata
  "setup_summary": "Two friends spend a day visiting an art museum in Florence, discussing paintings and planning where to eat lunch.",  # NEW
  "description_en": "...",
  ...
}
```

**Editorial Metadata Fields:**
- `setup_type`: One of "Arrival/Transaction", "Dialogue-Driven", "Problem-Solving", "Event/Preparation", "Narrative/Descriptive", "Discovery/Unexpected".
- `setup_summary`: A one-sentence description of the story's scenario, used to detect near-duplicates during reviews.

---

## 6. Review Workflow for User-Contributed Stories

When a user contributes a story (if this feature is added in v2+):

1. Automated validation:
   - Spell-check and grammar validation.
   - Word coverage check: what % of words are in the dictionary?
   - Language detection: confirm it matches the claimed target language.
   - Length validation: story meets word-count ranges for claimed difficulty.

2. Editorial review queue:
   - A content moderator or volunteer reviews the story against § 4.1 checklist.
   - If the story is too similar to an existing story, it is either rejected or suggested for refinement.
   - native-speaker feedback is sought for cultural and naturalness concerns.

3. Publication:
   - Upon approval, the story is added to the catalogue with editorial metadata.
   - The contributor is notified and credited (if applicable).

---

## 7. Acceptance Criteria

- [ ] Editorial checklist template exists and is used for all launch stories.
- [ ] All 27 launch stories pass the Pre-Submission checklist (§ 4.1).
- [ ] The launch catalogue passes the Launch Validation checklist (§ 4.2).
- [ ] Each story includes documented `setup_type` and `setup_summary` metadata.
- [ ] Within each language–difficulty combination, no two stories have overlapping `setup_summary` details.
- [ ] At least one story per language–difficulty tier uses a "Narrative/Descriptive" or "Discovery/Unexpected" setup to ensure variety beyond transaction-driven dialogues.

---

## 8. Success Metrics

- 100% of seeded stories meet content validation requirements at launch.
- Zero user reports of duplicate or overly similar story pairs within a month of launch.
- Learners report (in feedback) that stories feel varied and worth revisiting across difficulty levels.
