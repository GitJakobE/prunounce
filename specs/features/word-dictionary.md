# Feature Requirements Document — Word Dictionary & Categories

**Parent PRD:** [prd.md](../prd.md)
**Feature ID:** F-DICT
**Requirements:** REQ-2, REQ-11
**Priority:** P0 (Must-have for launch)

## 1. Overview

The application provides a curated dictionary of words in each supported target language (Italian, Danish, English), organised by thematic categories and difficulty levels. Each category–difficulty combination contains approximately 25 words, giving users a structured and progressive learning path. The word list is seeded from structured data files and grows through user contributions (see [user-contributed-words.md](user-contributed-words.md)).

## 2. User Stories

| ID | Story | Acceptance Criteria |
|---|---|---|
| US-D1 | As a learner, I want to browse words by category so I can focus on a topic that interests me. | A category list/grid is displayed; selecting a category shows its words in my target language. |
| US-D2 | As a learner, I want to filter words by difficulty so I can start at my level. | Within a category, I can select Beginner, Intermediate, or Advanced and see only words at that level. |
| US-D3 | As a learner, I want to see the target-language word, its phonetic hint, and translation at a glance. | Each word entry shows the word in my target language, a phonetic hint, and the translation in my reference language without extra clicks. |
| US-D4 | As a learner, I want to see how many words I've practised in a category so I can track progress. | A progress indicator (e.g., "12 / 25 practised") is visible per category–difficulty group. |
| US-D5 | As a learner of Danish, I want to see Danish words when I've selected a Danish host. | The dictionary shows words matching my current target language as determined by my host selection. |

## 3. Functional Requirements

### 3.1 Categories
- The dictionary must include at least 10 thematic categories at launch, per target language.
- Suggested categories (final list to be confirmed):
  1. Greetings & Basics
  2. Numbers & Counting
  3. Food & Drink
  4. Travel & Directions
  5. Shopping & Money
  6. Family & People
  7. Time & Calendar
  8. Weather & Nature
  9. Health & Body
  10. Common Verbs
- Category names must be localised to the user's reference language.
- Categories are shared across all target languages — the same 10+ categories exist for Italian, Danish, and English word sets.

### 3.2 Difficulty Levels
- Three fixed difficulty levels: **Beginner**, **Intermediate**, **Advanced**.
- Every word must be assigned exactly one difficulty level.
- Difficulty labels must be localised to the user's reference language.

### 3.3 Word Entries
Each word entry must contain:
- The word in its target language (canonical spelling).
- A phonetic hint (simplified pronunciation guide relevant to the target language).
- A translation in each supported reference language (Italian, Danish, English — minus the target language itself).
- A difficulty level assignment.
- A category assignment (a word may belong to more than one category).
- A source indicator: whether the word is seeded (curated) or user-contributed.

### 3.4 Multi-Language Word Sets
- Each target language has its own set of words. Italian words, Danish words, and English words are independent collections.
- The user's chosen host determines the target language, which determines which word set is displayed.
- When a user switches to a host in a different language, the dictionary view updates to show the corresponding word set.

### 3.5 Word Count
- Each category–difficulty combination should target approximately 25 words per target language.
- At launch the total dictionary should contain a minimum of 250 words per target language (10 categories × ~25 words).
- Total launch vocabulary: ~750+ words across all three languages.

### 3.6 Browsing Experience
- The main dictionary page shows all categories as a visual grid or list.
- Selecting a category opens a page showing the words within it, grouped or filterable by difficulty.
- Words should be displayed in a scannable list or card layout with the target-language word prominent, reference-language translation below, and a play button for audio.

### 3.7 Progress Indicators
- Each word the user has listened to at least once should be visually marked (e.g., checkmark or highlight).
- A summary count ("X / Y practised") should appear at the category and difficulty level.
- Progress is tracked per target language — switching languages shows separate progress.

### 3.8 Content Seeding
- The initial word dictionary must be loadable from structured seed files (e.g., JSON).
- Separate seed files per target language, or a combined file with a language field per entry.
- Each seed entry must contain: the word in its target language, phonetic hint, category, difficulty, translations for all reference languages, and example sentences with translations.
- Re-running the seed process must be idempotent — it must not create duplicate entries.
- The seed files should be version-controlled so that word list changes can be reviewed and tracked.

### 3.9 User-Contributed Word Integration
- Words added by users (see [user-contributed-words.md](user-contributed-words.md)) appear alongside seeded words in all views.
- There is no visual distinction between seeded and user-contributed words in the browsing experience.
- User-contributed words that are assigned to existing categories appear within those categories. Words without a category assignment appear in an "Uncategorised" grouping.

## 4. Edge Cases

- If a word belongs to multiple categories, it appears in each of those categories independently.
- If a category has fewer than 25 words at a given difficulty, it is still displayed; there is no minimum threshold to show a category.
- If the seed file contains a word that already exists in the system, the existing entry should be updated rather than duplicated.
- If a user switches target language, the category list remains but the words within each category change to match the new language.
- If a translation is missing for a word in a specific reference language, the English translation is shown as fallback with a visual indicator.

## 5. Acceptance Criteria

- [ ] At least 10 categories are available at launch, per target language.
- [ ] Each category contains words across Beginner, Intermediate, and Advanced levels.
- [ ] Each word displays the target-language word, phonetic hint, and reference-language translation.
- [ ] Words can be filtered by difficulty within a category.
- [ ] Progress indicators are visible per category–difficulty group.
- [ ] The total dictionary contains at least 250 unique words per target language at launch.
- [ ] The seed process can be run repeatedly without creating duplicate entries.
- [ ] Switching hosts/target language updates the word set accordingly.
- [ ] User-contributed words appear alongside curated words in all views.


### Audio Asset Processing Constraints
The system requires read-write access to its designated caching directory (e.g., udio-cache). Dynamic generated pronunciations MUST be written successfully to this directory on the flying before being served.
