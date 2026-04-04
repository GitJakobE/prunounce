# Feature Requirements Document — Progress Tracking

**Parent PRD:** [prd.md](../prd.md)
**Feature ID:** F-PROGRESS
**Requirement:** REQ-6
**Priority:** P1 (High — launch feature)

---

## 1. Overview

The system records which words a user has listened to and displays their learning progress. Progress is tracked per target language so that switching between languages shows separate, independent progress. Visual indicators on word cards and summary counts on category listings give users a clear sense of accomplishment and direction.

## 2. User Stories

| ID | Story | Acceptance Criteria |
|---|---|---|
| US-P1 | As a returning user, I want to see which words I've already listened to, so I can focus on new words. | Words I've previously played have a visual indicator (e.g., checkmark, highlight). |
| US-P2 | As a learner, I want to see how many words I've completed per category, so I can track my overall progress. | A summary count (e.g., "12 / 25 practised") is visible on each category card. |
| US-P3 | As a learner, I want to see progress broken down by difficulty within a category. | Within a category, I see per-difficulty progress (e.g., Beginner: 8/10, Intermediate: 3/10, Advanced: 1/5). |
| US-P4 | As a user who switched target languages, I want my progress for each language preserved separately. | Switching from an Italian host to a Danish host shows Danish progress; switching back shows Italian progress intact. |
| US-P5 | As a learner, I want to see my total progress across all categories. | A global progress summary shows overall words practised vs. total words available. |

## 3. Functional Requirements

### 3.1 Tracking Trigger
- A word is marked as "listened to" when the user plays its pronunciation audio at least once.
- The mark is permanent for that user — replaying the word does not remove the indicator.
- Only successful audio playback triggers the mark (not merely clicking a play button that fails).

### 3.2 Per-Word Indicators
- Each word card in category listings must show a visual indicator when the user has listened to it.
- The indicator must be unobtrusive but clearly visible (e.g., a subtle checkmark, muted colour change, or "listened" badge).

### 3.3 Category-Level Progress
- Each category in the category listing must display a progress summary showing the number of words practised out of the total in that category.
- Category names must be displayed in the user's reference language, not hardcoded to English.
- Optionally, a progress bar or percentage can supplement the count.

### 3.4 Difficulty-Level Progress
- Within a category view, progress should be shown per difficulty level (Beginner, Intermediate, Advanced).
- Each difficulty section shows its own "X / Y practised" count.

### 3.5 Global Progress Summary
- A summary view (e.g., on the main page or profile page) shows the user's total progress across all categories for the current target language.
- Example: "156 / 250 words practised in Italian."
- Category names in the progress view must be displayed in the user's reference language (e.g., Italian-reference users see "Saluti e basi" instead of "Greetings & Basics").

### 3.6 Per-Language Isolation
- Progress is tracked and displayed independently for each target language.
- If a user has practised 50 Italian words and 30 Danish words, switching to a Danish host shows 30, not 80.
- Switching back to an Italian host restores the Italian progress view.
- Progress for a language is never lost when switching to another language.

### 3.7 User-Contributed Words
- User-contributed words are included in progress tracking just like curated words.
- Listening to a user-contributed word marks it as practised.
- User-contributed words count toward category and global totals.

## 4. Edge Cases

- If new words are added to the dictionary (via seed update or user contribution) after a user has already tracked progress, the totals update to include the new words (e.g., "12 / 27 practised" instead of "12 / 25").
- If a user deletes their account, all progress data is permanently removed.
- If a word is listened to via search results (not category browsing), it is still marked as practised in the relevant category.

## 5. Acceptance Criteria

- [ ] Words the user has listened to show a visual "practised" indicator.
- [ ] Category cards show "X / Y practised" progress counts.
- [ ] Difficulty sections within a category show per-difficulty progress.
- [ ] A global progress summary shows total words practised for the current target language.
- [ ] Progress is tracked independently per target language.
- [ ] Switching target languages preserves progress for each language.
- [ ] User-contributed words are included in progress counts.
- [ ] Progress updates immediately after a word is listened to (no page reload required).
