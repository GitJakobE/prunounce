# Feature Requirements Document — User-Contributed Words

**Parent PRD:** [prd.md](../prd.md)
**Feature ID:** F-UGC
**Requirement:** REQ-9
**Priority:** P1 (Important for launch)

---

## 1. Overview

Logged-in users can add new words to the shared dictionary. Contributed words become part of the permanent word library and are visible to all users. When a user adds a word that does not already have cached TTS audio, the system automatically generates pronunciation audio for it. This feature enables the dictionary to grow organically beyond the curated seed data.

## 2. User Stories

| ID | Story | Acceptance Criteria |
|---|---|---|
| US-UGC1 | As a user, I want to add a new word in the target language so that I and others can practise its pronunciation. | A form allows entering a word, its translation, and optional category; the word appears in the dictionary after submission. |
| US-UGC2 | As a user who added a word, I want audio to be generated automatically so the word is immediately playable. | Within a few seconds of submission, the word has a playable pronunciation audio clip. |
| US-UGC3 | As a user, I want to provide a translation in my reference language when adding a word. | The word form requires at least one translation (in the user's current reference language). |
| US-UGC4 | As a user, I want to optionally assign a category and difficulty to the word I add. | The form offers optional category selection (from existing categories or "Uncategorised") and difficulty level. |
| US-UGC5 | As a learner, I want to see user-contributed words alongside curated words so the dictionary feels unified. | Contributed words appear in category listings, search results, and progress tracking just like seeded words. |
| US-UGC6 | As a user, I want to optionally add an example sentence when contributing a word. | The form includes optional fields for an example sentence in the target language and its translation. |

## 3. Functional Requirements

### 3.1 Word Submission Form
- Accessible from the main navigation or a prominent "Add Word" button on the categories page.
- Required fields:
  - **Word** in the current target language
  - **Translation** in the user's current reference language
- Optional fields:
  - **Phonetic hint** (free text)
  - **Category** (dropdown of existing categories, defaults to "Uncategorised")
  - **Difficulty** (Beginner / Intermediate / Advanced, defaults to Beginner)
  - **Example sentence** in the target language
  - **Example sentence translation** in the reference language
- The form must validate that the word field is not empty and does not already exist in the dictionary for the current target language (case-insensitive).
- On successful submission, the user sees a confirmation and the word is immediately available in the dictionary.

### 3.2 Audio Generation
- When a new word is submitted, the system checks whether a cached TTS audio file exists for that word in the target language.
- If no audio exists, the system generates it using the same TTS service (Microsoft Edge TTS) and voice used by the user's current host persona.
- Audio generation happens asynchronously after submission; the word entry is created immediately. If audio is not yet ready when a user tries to play it, a brief loading indicator is shown.
- Generated audio is cached and shared — subsequent plays by any user use the cached file.

### 3.3 Data Model
- User-contributed words are stored in the same dictionary table as seeded words.
- A field indicates whether the word was seeded or user-contributed, and who contributed it.
- Contributed words that are missing translations in some reference languages display an English fallback (consistent with the multi-language support FRD).

### 3.4 Visibility
- User-contributed words are visible to all users, not just the contributor.
- They appear in category listings, search results, and progress tracking identically to seeded words.
- There is no separate "user words" section — contributed words are integrated into the main dictionary.

### 3.5 Duplicate Prevention
- Before adding a word, the system checks for an existing entry with the same spelling in the same target language (case-insensitive, ignoring diacritical marks).
- If a duplicate is found, the user is informed and the submission is rejected with a link to the existing word.

## 4. Edge Cases

- If TTS audio generation fails (service unavailable), the word is still saved but marked as "audio pending." The system should retry audio generation on the next access attempt.
- If a user contributes a word with only one translation, the word is visible to users with that reference language. Users with a different reference language see the English fallback or a "translation not available" indicator.
- Very long words or phrases (> 100 characters) should be rejected with a validation error.
- Words containing only numbers, special characters, or whitespace should be rejected.

## 5. Acceptance Criteria

```gherkin
Given I am a logged-in user on the categories page,
When I click "Add Word",
Then I see a form with fields for word, translation, and optional category/difficulty/example.
```

```gherkin
Given I fill in a valid word and translation,
When I submit the form,
Then the word appears in the dictionary immediately,
And TTS audio is generated within a few seconds.
```

```gherkin
Given I try to add a word that already exists in the dictionary,
When I submit the form,
Then I see an error message indicating the word already exists.
```

```gherkin
Given another user contributed a word,
When I browse the dictionary or search for it,
Then I see it alongside curated words with no visible distinction.
```

```gherkin
Given I added a word with an example sentence,
When I play the word's audio,
Then the example sentence audio plays automatically after the word pronunciation.
```
