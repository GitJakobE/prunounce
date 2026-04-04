# Feature Requirements Document — Story Reading

**Parent PRD:** [prd.md](../prd.md)
**Feature ID:** F-STORY
**Priority:** P1 (Post-launch enhancement)

---

## 1. Overview

Story Reading is a new top-level learning mode alongside the existing word Categories section. Users choose between "Categories" (word-by-word pronunciation practice) and "Stories" (reading comprehension with host narration). Stories are curated, themed texts written in the user's target language, organised by difficulty level, and narrated by the user's selected host at a user-chosen speed. An integrated translation panel lets users click any word in the story to see its translation, phonetic hint, and hear its pronunciation — bridging reading practice with the existing dictionary.

## 2. User Stories

| ID | Story | Acceptance Criteria |
|---|---|---|
| US-S1 | As a learner, I want to choose between Categories and Stories from a top-level navigation, so that I can pick the learning mode that suits me. | After host selection, the main page presents two clear entry points: "Categories" and "Stories". |
| US-S2 | As a learner, I want to browse stories organised by difficulty level, so that I can pick stories appropriate for my skill. | The Stories section groups stories under Beginner, Intermediate, and Advanced headings. |
| US-S3 | As a learner, I want to read a full story in my target language, so that I can practise reading comprehension. | Selecting a story opens a reading view showing the full story text in the target language. |
| US-S4 | As a learner, I want to have my host read the story aloud, so that I can hear correct pronunciation of connected speech. | A play button starts narration of the full story text using the user's selected host's TTS voice. |
| US-S5 | As a learner, I want to control the narration speed, so that I can slow down for difficult passages or speed up when I'm comfortable. | A speed control offers 5 distinct speeds; the selected speed applies immediately to the current narration. |
| US-S6 | As a learner, I want to click any word in the story and see its translation, so that I can understand unfamiliar words without leaving the page. | Clicking a word in the story text populates the translation panel with that word's translation in the user's reference language. |
| US-S7 | As a learner, I want to see a phonetic hint for the clicked word, so that I can understand how to pronounce it. | The translation panel shows a phonetic hint alongside the translation. |
| US-S8 | As a learner, I want to hear the pronunciation of a clicked word, so that I can learn individual words while reading. | The translation panel includes a play button that pronounces the clicked word using the host's TTS voice. |
| US-S9 | As a learner, I want stories themed around real-life situations, so that I learn vocabulary and phrases I can actually use. | Each story is set in a practical, relatable scenario (e.g., ordering food, visiting a market, asking for directions). |
| US-S10 | As a learner, I want to see at least 3 stories per difficulty level in my target language, so that I have enough content to practise with. | At launch, each target language has at minimum 3 stories per difficulty level (9 stories per language, 27 total). |
| US-S11 | As a learner, I want short stories to feel genuinely shorter and simpler than long stories, so that choosing a difficulty changes the scope and effort of the reading task. | Beginner, Intermediate, and Advanced stories differ in narrative scope, progression, and information density, not only by approximate word count. |
| US-S12 | As a learner, I want stories to begin from different kinds of situations, so that the library feels varied instead of repetitive. | The story catalogue includes varied setup patterns, settings, and opening situations within each language instead of repeatedly using the same opening template. |

## 3. Functional Requirements

### 3.1 Top-Level Navigation

- After host selection, the main page must present two equally prominent entry points: **Categories** and **Stories**.
- Both options must be visually balanced — neither should appear as the primary or secondary choice.
- The navigation labels must be localised to the user's reference language.
- The existing host banner (portrait, name, greeting) remains visible on this top-level page.

### 3.2 Story Library

- The Stories section displays all available stories for the user's current target language (determined by their host).
- Stories are grouped by difficulty level: **Beginner**, **Intermediate**, **Advanced**.
- Difficulty labels must be localised to the user's reference language.
- Each story is presented as a card showing:
  - The story title (in the target language)
  - A short description or theme hint (in the reference language)
  - The difficulty level badge
  - An estimated reading time
- Selecting a story card opens the full story reading view.

### 3.3 Story Content

- Each story is a curated, themed text written entirely in the target language.
- Stories must be themed around practical, real-life situations that reinforce useful vocabulary, while still allowing a mix of dialogue-driven, descriptive, reflective, and event-driven pieces. Example themes:
  - **Beginner:** Introducing yourself at a café, shopping at a market, asking for directions
  - **Intermediate:** A day at a museum, ordering a meal and discussing ingredients, a visit to the doctor
  - **Advanced:** Negotiating at a flea market, telling a folk tale, debating weekend plans with friends
- Story length guidelines:
  - **Beginner:** approximately 100–150 words
  - **Intermediate:** approximately 200–300 words
  - **Advanced:** approximately 400–600 words
- Story length tiers must differ in more than word count:
  - **Beginner:** one clear scenario, limited cast, one primary objective or exchange, and tightly constrained vocabulary load.
  - **Intermediate:** at least one meaningful development beyond the opening setup, such as a complication, choice, misunderstanding, or short sequence of events.
  - **Advanced:** a broader narrative arc with multiple beats, richer description or reflection, and enough development that the story cannot be reduced to a slightly extended beginner pattern.
- The opening setup of stories must vary across the catalogue. The library must not overuse a single repeated pattern such as repeatedly starting with a near-identical arrival, greeting, or service interaction that only changes surface details.
- Within each language, stories across a difficulty tier should cover a mix of setup types, for example: arriving somewhere, solving a small problem, preparing for an event, recounting something that already happened, discovering something unexpected, or helping another person.
- At launch, the minimum set of 3 stories per difficulty level per language must represent at least 3 distinct setups per level rather than three close variations of the same premise.
- Each story must have a title in the target language.
- Each story must have a short description/theme summary in all supported reference languages.
- At launch: **3 stories per difficulty level per target language** (9 stories per language × 3 languages = 27 stories total).

### 3.4 Story Reading View

- The reading view displays the full story text in the target language.
- The text must be rendered with generous line spacing and a readable font size to support comfortable reading.
- Every word in the story text must be individually clickable/tappable.
- Clicked words must be visually highlighted (e.g., background colour or underline) to show which word is selected.
- A **translation panel** is displayed to the right of the story text on desktop, or as a slide-up panel on mobile.

### 3.5 Translation Panel

- The translation panel is a persistent, fixed-position box alongside the story text.
- When no word is selected, the panel displays a prompt such as "Click any word to see its translation."
- When a word is clicked, the panel updates to show:
  - **The word** in the target language (as displayed in the text)
  - **The translation** in the user's currently selected reference language (as stored in their profile — never hardcoded to a single language)
  - **A phonetic hint** (simplified pronunciation guide)
  - **A play button** that pronounces the word using the user's selected host's TTS voice
- Word lookup uses the existing dictionary as the primary source. If the word exists in the dictionary, its stored translation and phonetic hint are displayed.
- If a clicked word is not found in the curated dictionary, the system must attempt an on-the-fly translation and audio generation as described in [on-the-fly-word-lookup.md](on-the-fly-word-lookup.md) (REQ-18). Auto-translated results must be visually distinguished from curated entries. Only if on-the-fly lookup also fails should the panel display a "Translation temporarily unavailable" message.
- The play button in the panel must follow the same audio behaviour as word pronunciation elsewhere in the app (< 1 s latency, cached per host+word, stops other playing audio).

### 3.6 Host Narration (Read Aloud)

- A clearly visible **play/pause button** allows the user to have the host read the entire story aloud.
- Narration uses the user's selected host's TTS voice, matching the same voice used for word pronunciation.
- The narration reads the full story text from beginning to end.
- **Five speed settings** must be available:
  - **Very Slow** — significantly reduced speed for beginners parsing each word
  - **Slow** — reduced speed for careful listening
  - **Normal** — natural conversational pace
  - **Fast** — slightly accelerated for intermediate/advanced practice
  - **Very Fast** — noticeably accelerated for advanced comprehension training
- The speed selector must be accessible before and during narration; changing speed takes effect immediately without restarting from the beginning.
- A **stop button** resets narration to the beginning of the story.
- While narration is playing, the currently spoken word or sentence should be visually highlighted in the text (karaoke-style tracking), so the user can follow along.
- If the user clicks a word's play button in the translation panel while narration is active, narration pauses, the individual word plays, and narration can be resumed.

### 3.7 Responsive Layout

- **Desktop:** Story text occupies approximately 70% of the reading area width; the translation panel occupies approximately 30%, positioned to the right.
- **Tablet:** Same side-by-side layout as desktop if screen width permits; otherwise, translation panel appears as a collapsible overlay at the bottom.
- **Mobile:** Story text is full-width. The translation panel appears as a slide-up sheet from the bottom when a word is tapped, and can be dismissed by swiping down or tapping outside.

### 3.8 Content Seeding

- Stories must be loadable from structured seed files, alongside the existing word dictionary seeding.
- Each story seed entry must contain:
  - A unique story identifier
  - The target language code
  - The difficulty level
  - The story title (in the target language)
  - A short description in each supported reference language
  - The full story text (in the target language)
- Seeded story content must include enough editorial metadata or review context for content authors to confirm that each story's setup type and narrative scope are distinct from other stories in the same language-level group.
- The seed process must be idempotent — re-running it must not create duplicate stories.
- Story seed files should be version-controlled.

### 3.9 Multi-Language Support

- Stories are specific to a target language — Italian stories are written in Italian, Danish stories in Danish, English stories in English.
- Switching hosts to a different language shows the story library for that language.
- Story titles are in the target language; descriptions and UI labels are in the user's reference language.
- The translation panel translates clicked words into the user's reference language.

## 4. Edge Cases

- If a word in the story is not found in the dictionary, the translation panel displays "Translation not available" rather than an error.
- If TTS is temporarily unavailable, narration and word play buttons show a user-friendly error: "Audio temporarily unavailable. Please try again shortly."
- Punctuation attached to words (e.g., commas, periods, question marks) must be stripped when performing the dictionary lookup, but kept in the displayed text.
- Hyphenated words or contractions should be looked up as a whole first; if not found, look up each part separately.
- If the user switches hosts (and therefore target language) while reading a story, they should be returned to the Stories library for the new language.
- Very long stories must remain performant — word click targets must not degrade on stories with 600+ words.
- If two seeded stories in the same language and difficulty share substantially the same opening premise, setting, and progression shape, they should be treated as a content-quality issue rather than acceptable variety.

## 5. Acceptance Criteria

- [ ] A top-level navigation presents "Categories" and "Stories" as equal choices after host selection.
- [ ] The Stories section shows stories grouped by Beginner, Intermediate, and Advanced difficulty.
- [ ] At launch, each target language has at least 3 stories per difficulty level (9 per language).
- [ ] Selecting a story opens a reading view with the full text in the target language.
- [ ] Beginner, Intermediate, and Advanced stories are observably different in scope and progression, not only in total word count.
- [ ] Within each target language and difficulty level, the launch set avoids repeated opening setups and includes distinct story premises.
- [ ] Every word in the story text is individually clickable.
- [ ] Clicking a word populates the translation panel with the word's translation in the user's currently selected reference language (not a hardcoded default), a phonetic hint, and a play button.
- [ ] Switching the reference language via the language switcher immediately affects subsequent word lookups — new clicks show translations in the newly selected language.
- [ ] The play button in the translation panel pronounces the word using the host's TTS voice within 1 second.
- [ ] A play/pause button starts host narration of the full story.
- [ ] Five narration speed settings are available and can be changed during playback without restarting.
- [ ] The currently narrated portion of text is visually highlighted during playback.
- [ ] A stop button resets narration to the beginning.
- [ ] Playing an individual word from the translation panel pauses active narration.
- [ ] The translation panel is positioned to the right on desktop and as a slide-up sheet on mobile.
- [ ] Stories are seeded from structured seed files idempotently.
- [ ] Switching hosts updates the story library to the new target language.
- [ ] Words not found in the dictionary display "Translation not available" in the panel.
- [ ] Navigation labels and difficulty labels are localised to the user's reference language.
