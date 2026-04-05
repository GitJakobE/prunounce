# Task 066 — End-to-End Verification of Story Cleanup

**Feature:** [story-seed-cleanup.md](../features/story-seed-cleanup.md)  
**Priority:** P1  
**Dependencies:** Task 063, Task 064, Task 065  

---

## Description

After the seeder fix (Task 063), database cleanup (Task 064), and test updates (Task 065) are complete, a final verification must confirm the story library meets the FRD acceptance criteria end-to-end: correct story counts, full audio coverage, no orphaned data, and correct UI rendering.

## Technical Requirements

- Run `verify_story_assets.py` and confirm zero missing audio and zero missing words.
- Query the database to confirm:
  - Exactly **27 short stories** (3 languages × 3 levels × 3 stories each).
  - Zero stories for unsupported languages (`es`).
  - Every short story has ≥ 1 StoryAudio row.
- Verify the stories API endpoint returns the correct counts per language/level.
- Verify the frontend story library page renders exactly 3 short stories per level per language, all with a functional play button.

## Acceptance Criteria

| # | Criterion |
|---|---|
| 1 | `verify_story_assets.py` reports `audio_missing=0`. |
| 2 | Database query: `SELECT COUNT(*) FROM Story WHERE length='short'` = **27**. |
| 3 | Database query: `SELECT COUNT(*) FROM Story WHERE language='es'` = **0**. |
| 4 | Stories API returns exactly 3 short stories per level for each of en, da, it. |
| 5 | All existing tests pass: `poetry run pytest` exits with code 0. |
| 6 | Frontend story library shows 3 playable short stories per level per language. |

## Testing Requirements

- This task is a verification gate, not a code-change task.
- Run the full test suite (`poetry run pytest`) and confirm all pass.
- Run `verify_story_assets.py` and capture output.
- Manual or automated spot-check of the frontend story list page.
