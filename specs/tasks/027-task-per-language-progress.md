# Task 027: Per-Language Progress Tracking

**Feature:** F-PROGRESS (Progress Tracking)
**Priority:** P1
**Dependencies:** 017 (Schema Migration), 019 (Multi-Language Dictionary API)

## Description

Update progress tracking so that progress is displayed independently per target language. The existing `UserProgress` model already tracks per-word progress, and since words now have a `language` field, progress is implicitly per-language. This task ensures the API and frontend correctly scope progress display to the current target language.

## Technical Requirements

### Backend: Progress Scoping
- The categories endpoint already joins `UserProgress` to count listened words — ensure the count only includes words matching the user's current target language
- The words endpoint already returns `listened` per word — this naturally scopes to the target language since the words themselves are filtered by language

### Backend: Global Progress Endpoint
- Add a `GET /api/progress` endpoint (or extend the existing categories endpoint response) that returns:
  - `totalWords` — total words in the user's current target language
  - `listenedWords` — words listened to by the user in the current target language
  - Per-category breakdown with listened counts

### Frontend: Progress Display
- The categories page shows progress counts scoped to the target language
- The profile page (if it shows global progress) should reflect the current target language
- When the user switches hosts to a different language, progress counts update to show progress for the new target language
- Previously accumulated progress for the old language is preserved and shown when the user switches back

### Frontend: Progress Summary
- Display a global progress summary on the main page or profile page: "X / Y words practised in [Language]"
- The language name should be localised to the reference language

## Acceptance Criteria

- [ ] Progress counts on the categories page reflect only the current target language
- [ ] Switching to a different target language shows separate progress for that language
- [ ] Switching back restores the original language's progress
- [ ] Global progress summary shows total/listened for the current target language
- [ ] Progress for user-contributed words is tracked the same as curated words
- [ ] Progress data is never lost when switching between languages

## Testing Requirements

- Progress endpoint returns counts scoped to the target language
- A user with progress in Italian sees different counts in Danish
- Switching hosts updates progress display
- User-contributed words count toward progress totals
