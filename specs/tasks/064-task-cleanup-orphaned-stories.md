# Task 064 — Database Cleanup Script for Orphaned Stories

**Feature:** [story-seed-cleanup.md](../features/story-seed-cleanup.md)  
**Priority:** P1  
**Dependencies:** Task 063  

---

## Description

Existing databases already contain the 36 audio-less stories inserted by earlier runs of `seed_data.py`. A one-time cleanup script must remove these orphaned stories and any associated records (StoryAudio rows, if any) from the database. The script must be safe to run on both databases that have the orphaned stories and databases that do not.

## Technical Requirements

- Create a script (e.g., `cleanup_orphaned_stories.py`) in `src/backend-python/` that:
  1. Identifies all Story rows that have **zero associated StoryAudio rows**.
  2. Also identifies all Story rows for languages that do not have a configured host persona (currently: `es` / Spanish).
  3. Deletes those Story rows. The `StoryAudio` FK has `ondelete="CASCADE"` so any stray audio rows will be cleaned automatically.
  4. Prints a summary of what was deleted (count per language, slugs removed).
- The script must be idempotent — running it twice produces no errors and no additional deletions.
- The script must **not** delete stories that have audio (the 27 canonical stories from `seed_stories.py`).
- The script should use the existing `app.database.SessionLocal` and `app.models` imports.

## Acceptance Criteria

| # | Criterion |
|---|---|
| 1 | After running the script on a database with orphaned stories, querying `Story` where `length = 'short'` returns exactly **27 rows** (3 languages × 3 levels × 3 stories). |
| 2 | No Story rows exist for language `es`. |
| 3 | Every remaining Story row has **≥ 1** associated StoryAudio row. |
| 4 | Running the script a second time deletes zero rows and exits cleanly. |
| 5 | Medium and long stories with audio are untouched. |

## Testing Requirements

- Unit test: script correctly identifies stories with zero audio in a test database.
- Unit test: script does not delete stories that have associated audio.
- Unit test: script is idempotent (second run = zero deletions).
- Test coverage ≥ 85%.
