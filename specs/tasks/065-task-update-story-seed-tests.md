# Task 065 — Update Story Seed Tests

**Feature:** [story-seed-cleanup.md](../features/story-seed-cleanup.md)  
**Priority:** P1  
**Dependencies:** Task 063, Task 064  

---

## Description

The existing `test_story_seed.py` validates `stories.json` structure and tests the `seed_data.py` story seeder. Since Task 063 removes story seeding from `seed_data.py`, these tests must be updated to reflect the new single-source-of-truth model where `seed_stories.py` is the only story seeder.

## Technical Requirements

- **Remove or update** the `TestStoriesJsonStructure` test class:
  - The `stories.json` file belongs to the old Node.js backend and is no longer consumed by the Python backend for seeding. Tests that validate its structure are no longer relevant to the Python backend's correctness.
  - Either remove the class entirely, or move it to an optional/separate test module if the file should still be validated for the Node.js backend.

- **Remove or update** the `TestSeedStories` integration test class:
  - `test_seeder_creates_all_stories` — should no longer test `seed_data.seed_stories()` against `stories.json`.
  - `test_seeder_is_idempotent` — same.
  - `test_seeder_updates_existing_story_on_rerun` — same.
  - `test_seeder_creates_stories_for_all_languages` — same.

- **Add new tests** that validate `seed_stories.py` as the authoritative seeder:
  - Test that `seed_stories.py` creates exactly 81 Story rows (27 slugs × 3 languages).
  - Test that every story created by `seed_stories.py` has a non-empty `length` field (not defaulting to "short" unintentionally).
  - Test that `seed_stories.py` is idempotent.
  - Test that for each (language, difficulty, length) combination where length = "short", there are exactly 3 stories.
  - Test that `seed_data.py` no longer creates any Story rows.

## Acceptance Criteria

| # | Criterion |
|---|---|
| 1 | All tests pass with `poetry run pytest`. |
| 2 | No test references `seed_data.seed_stories()` for story seeding validation. |
| 3 | The new test suite validates the 81-story invariant from `seed_stories.py`. |
| 4 | The 3-per-language-per-level-per-length invariant is tested for short stories. |
| 5 | Test coverage for story seeding ≥ 85%. |

## Testing Requirements

- This task **is** the testing task — the deliverable is a corrected and expanded test suite.
- All new tests must pass on a clean database.
- Tests must not depend on execution order.
