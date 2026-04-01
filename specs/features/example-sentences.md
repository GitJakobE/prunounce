# Feature Requirements Document: Contextual Example Sentences

**Parent PRD:** [prd.md](../prd.md)
**Feature ID:** F-EXAMPLES
**Requirement:** REQ-10

---

## 1. Overview

Every word in the dictionary includes an example sentence in the target language that uses the word in natural context, along with translations into each reference language (Italian, Danish, and English). The example sentence is displayed visually on the word card and played as audio automatically after the word's pronunciation, reinforcing both pronunciation and comprehension.

## 2. Example Sentence Content

- Each word entry includes:
  - An example sentence in the word's target language containing the word
  - Translations of the example sentence into all other supported languages (so they can serve as reference translations regardless of which reference language the user has selected)
- Example sentences for curated words are included in the seed data and loaded during the seeding process.
- Sentences are short, natural, and appropriate for the word's difficulty level.
- User-contributed words may optionally include example sentences (see [user-contributed-words.md](user-contributed-words.md)). If omitted, the example section is gracefully hidden.

## 3. Visual Display

- The word card shows the example sentence in the target language in italics below the word's translation.
- The reference-language translation of the example is displayed beneath the target-language sentence in smaller text.
- Examples are only shown when available (gracefully hidden if missing).

## 4. Audio Playback

- When a user plays a word's pronunciation, the system plays:
  1. The word pronunciation audio (in the target language, using the host's voice)
  2. A brief pause (~600 ms)
  3. The example sentence audio (in the same target language, using the same host's voice)
- Both audio clips are pre-generated and cached (same mechanism as word audio, per host voice).
- The sequential playback is interruptible — clicking another word stops the current chain.
- The example audio endpoint is separate from the word audio endpoint.

## 5. Acceptance Criteria

```gherkin
Given I am learning Italian and viewing a word card for "ciao",
When I look at the card details,
Then I see the Italian example sentence in italics (e.g., "Ciao, come stai?"),
And I see the translation in my reference language below it.
```

```gherkin
Given I am learning Danish and viewing a word card for "hygge",
When I look at the card details,
Then I see a Danish example sentence using "hygge",
And I see the translation in my reference language below it.
```

```gherkin
Given I click the play button on a word with an example sentence,
When the word pronunciation finishes,
Then the example sentence audio plays automatically after a short pause,
And the audio uses the same host voice as the word pronunciation.
```

```gherkin
Given the example sentence is playing,
When I click play on a different word,
Then the current playback stops and the new word begins playing.
```

```gherkin
Given a word has no example sentence (e.g., a user-contributed word without one),
When I view the word card,
Then no example section is shown,
And only the word pronunciation plays on click.
```
