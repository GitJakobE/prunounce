# Feature Requirements Document — Content Quality Assurance

**Parent PRD:** [prd.md](../prd.md)
**Feature ID:** F-CONTENT-QA
**Priority:** P1 (Content integrity)
**Related:** [story-reading.md](story-reading.md), [story-dialogue-formatting.md](story-dialogue-formatting.md), [word-dictionary.md](word-dictionary.md), REQ-11, REQ-14

---

## 1. Overview

Pronuncia's educational value depends directly on the accuracy of its content — story text, grammar, translations, phonetic hints, and TTS pronunciation. Errors in any of these undermine learner trust and can teach incorrect language. Currently, there is no systematic process for validating content quality before it goes live, and no mechanism for flagging issues after publication.

This feature introduces a **content quality assurance system** that catches and prevents grammatical errors, incorrect translations, pronunciation mismatches, and formatting issues across all seeded and user-contributed content. It combines automated validation checks that run before content is published with a user-facing reporting mechanism so learners can flag problems they encounter.

## 2. Problem Statement

- Story text contains grammatical errors, misspellings, and incorrect word usage that are not caught before publication.
- TTS pronunciation of certain words or names produces incorrect or unnatural results, but there is no way to know without manually listening to every audio clip.
- Phonetic hints in the word dictionary may not match how TTS actually pronounces a word.
- Translations may be inaccurate, missing, or inconsistent across reference languages.
- There is no feedback loop — users who notice errors have no way to report them, so issues persist indefinitely.
- As the content library grows (more stories, more user-contributed words), manual spot-checking becomes unsustainable.

## 3. User Stories

| ID | Story | Acceptance Criteria |
|---|---|---|
| US-QA1 | As a content author, I want automated checks to catch spelling and grammar errors in story text before publishing, so that learners never see broken content. | Story text is validated against language-appropriate rules before being committed to the database. |
| US-QA2 | As a content author, I want to verify that every word in a story can be looked up in the dictionary, so that the translation panel works for all clickable words. | A validation report lists story words with no dictionary match. |
| US-QA3 | As a content author, I want to preview TTS pronunciation of story text before publishing, so that I can catch awkward or incorrect pronunciations. | An author can trigger a preview narration of unpublished story content. |
| US-QA4 | As a learner, I want to report an error I notice in a story or word entry, so that it can be reviewed and fixed. | A report button is available on story and word views; submitting a report captures the context (which story/word, what the issue is). |
| US-QA5 | As a content reviewer, I want to see a list of all reported content issues, so that I can prioritise and address them. | A review dashboard or report lists pending error reports with their context. |
| US-QA6 | As a content author, I want translation consistency checks across all three reference languages, so that no translations are missing or obviously mismatched. | A validation report flags entries where one or more translations are empty or suspiciously short/long compared to others. |
| US-QA7 | As a learner, I want confidence that the content I'm learning from has been reviewed, so that I can trust the accuracy of what I hear and read. | Published stories and words have passed a defined quality gate before being visible. |

## 4. Functional Requirements

### 4.1 Automated Content Validation (Pre-Publish Checks)

The system must provide a validation pipeline that can be run against content before it is committed or seeded. These checks operate on story text, word entries, translations, and phonetic hints.

#### 4.1.1 Story Text Validation

- **Spelling check**: Validate that all words in a story's body text are correctly spelled for the story's target language.
- **Grammar check**: Flag common grammatical issues (e.g., subject-verb agreement, incorrect article usage, tense consistency).
- **Word coverage check**: For every unique word token in a story, verify whether a matching entry exists in the word dictionary. Report uncovered words — these are words that will show "Translation not available" when clicked.
- **Dialogue format check** (for dialogue stories): Verify that every dialogue line has a valid speaker label, that speaker labels are consistent throughout the story, and that each story has no more than 4 speakers.
- **Length check**: Verify that story word count falls within the guidelines for its difficulty level.

#### 4.1.2 Word Dictionary Validation

- **Translation completeness**: Every word entry must have a non-empty translation in all three reference languages (English, Danish, Italian). Flag entries with missing translations.
- **Phonetic hint presence**: Every word entry must have a non-empty phonetic hint. Flag entries with missing hints.
- **Translation plausibility**: Flag translations where the length ratio between the source word and its translation is extreme (e.g., a single Italian word translated as a 10-word English phrase, or vice versa) — this may indicate a copy-paste error or incorrect entry.
- **Duplicate detection**: Flag word entries that appear to be near-duplicates (e.g., same word with slightly different spellings or an extra space).
- **Example sentence presence**: Flag word entries that have no example sentence in any language.

#### 4.1.3 Pronunciation Validation

- **TTS pronunciation audit**: Provide a mechanism to generate and listen to TTS audio for story text or individual words, enabling a human reviewer to verify pronunciation quality.
- **Known mispronunciation list**: Maintain a list of words or names where TTS produces known incorrect pronunciations, along with the recommended workaround (e.g., SSML phoneme tags, respelling).
- **Audio file integrity**: For pre-generated audio files, verify that the file exists, is non-zero in size, and is a valid audio format.

### 4.2 User Error Reporting

Learners who encounter errors in stories or word entries must be able to report them without leaving the learning flow.

#### 4.2.1 Report Mechanism

- A **report button** (e.g., flag icon) must be available on:
  - The story reading view (to report story-level issues: grammar, awkward phrasing, wrong narration)
  - The translation panel (to report word-level issues: wrong translation, wrong phonetic hint, bad pronunciation)
  - The word card in categories view (same as above)
- Tapping the report button opens a **lightweight report form** that captures:
  - The **content type** being reported (story or word) — auto-populated
  - The **specific item** (story title/slug or word text) — auto-populated
  - An **error category** (selectable): Grammar / Spelling, Wrong Translation, Pronunciation Issue, Formatting Issue, Other
  - A **free-text description** (optional, up to 500 characters) where the user can describe the issue
- The report is submitted with a single tap after selecting a category. The free-text field is optional to minimise friction.
- After submitting, the user sees a brief confirmation ("Thanks for reporting — we'll review this") and can continue learning.
- Users must be logged in to submit reports (to prevent spam and enable follow-up).

#### 4.2.2 Report Data

- Each report must record:
  - Report ID
  - Reporting user ID
  - Content type (story / word)
  - Content identifier (story ID or word ID)
  - Error category
  - Free-text description (if provided)
  - Timestamp
  - Status (new / reviewed / resolved / dismissed)
- Duplicate reports for the same content item from the same user should be prevented (one active report per user per item).

### 4.3 Content Review Dashboard

- A review interface should present all pending error reports, ordered by recency or frequency (multiple users reporting the same issue indicates higher priority).
- Each report entry must show: the content item, error category, user description, number of reports for the same item, and current status.
- A reviewer can update the status of a report (reviewed → resolved or dismissed) and optionally add a resolution note.
- The dashboard should support filtering by: content type, error category, status, and language.

### 4.4 Quality Gate for Seeded Content

- Before new story or word seed data is merged or deployed, the automated validation checks (4.1) must pass without critical errors.
- Critical errors (e.g., missing translations, empty story body, words outside length guidelines) must block publication.
- Warnings (e.g., uncovered words, extreme translation length ratios) should be flagged for review but not block publication.
- The validation pipeline must be runnable as a standalone script (for content authors to check locally) and as part of any automated deployment process.

## 5. Content Review Process

The quality assurance workflow operates at two stages:

### 5.1 Pre-Publication (Proactive)

1. Content author creates or updates story/word seed data.
2. Author runs the automated validation script locally.
3. Script produces a report listing errors (must-fix) and warnings (should-review).
4. Author fixes all errors and reviews all warnings.
5. Author uses the TTS preview mechanism to listen to narration and spot-check pronunciation.
6. Content passes validation and is committed to the seed files.

### 5.2 Post-Publication (Reactive)

1. Learners encounter issues while using the app.
2. Learners submit error reports via the report button.
3. Reports appear in the content review dashboard.
4. Content reviewer triages reports: investigates, confirms or dismisses the issue.
5. For confirmed issues, the reviewer updates the seed data and re-runs validation.
6. Corrected content is redeployed; the report is marked as resolved.

## 6. Edge Cases

- If the spelling/grammar check service is unavailable, validation should report the check as skipped rather than failing the entire pipeline.
- User reports about subjective quality (e.g., "this story is boring") should be dismissible without further action.
- Reports against user-contributed words should be tied to the word entry, not the contributing user — editorial fixes do not penalise contributors.
- If a word in a story is intentionally non-standard (e.g., a dialectal form, a proper noun), it should be possible to add it to an exception list so it doesn't trigger validation warnings on every run.
- TTS pronunciation issues that cannot be fixed (due to TTS engine limitations) should be documented in the known mispronunciation list so reviewers don't re-investigate the same problems.

## 7. Acceptance Criteria

- [ ] An automated validation script can be run against story seed data and produces a report of errors and warnings.
- [ ] The script checks: spelling, word coverage against the dictionary, story length vs. difficulty guidelines, dialogue format consistency, and translation completeness.
- [ ] Word dictionary validation checks: translation completeness, phonetic hint presence, duplicate detection, and example sentence presence.
- [ ] Critical validation errors block content publication; warnings are flagged for review.
- [ ] A report button is available on story reading view, translation panel, and word cards.
- [ ] The report form captures content type, item identifier, error category, and optional free-text — auto-populating what it can.
- [ ] Submitting a report shows confirmation and does not interrupt the learning flow.
- [ ] Duplicate reports from the same user for the same item are prevented.
- [ ] A content review dashboard lists all pending reports with filtering by type, category, status, and language.
- [ ] Report status can be updated (reviewed / resolved / dismissed) with an optional resolution note.
- [ ] The validation script is runnable locally by content authors and as part of automated checks.
- [ ] A known mispronunciation list exists for documenting TTS issues that cannot be programmatically fixed.
