# Task 063 — Remove Story Seeding from `seed_data.py`

**Feature:** [story-seed-cleanup.md](../features/story-seed-cleanup.md)  
**Priority:** P1  
**Dependencies:** None  

---

## Description

The `seed_data.py` script seeds stories from `src/backend/data/stories.json` — a data file belonging to the old Node.js backend. These 36 stories duplicate the short-story slots already filled by the authoritative `seed_stories.py` seeder, and none of them have narration audio. The `seed_data.py` seeder must stop inserting stories so that re-running it no longer re-introduces audio-less duplicates.

## Technical Requirements

- Remove the `seed_stories(db, stories_data)` call and the `stories_data = load("stories.json")` line from `seed_data.py`'s `main()` function.
- Remove or keep the `seed_stories()` helper function in `seed_data.py` — if no other caller uses it, remove it to avoid dead code.
- The remaining word/category seeding in `seed_data.py` must continue to work unchanged.
- `seed_stories.py` remains the single authoritative source for all story content.

## Acceptance Criteria

| # | Criterion |
|---|---|
| 1 | Running `poetry run python seed_data.py` on a fresh database seeds words and categories but creates **zero** Story rows. |
| 2 | Running `poetry run python seed_stories.py` after `seed_data.py` produces the expected story count (81 rows: 27 unique stories × 3 languages). |
| 3 | Running `seed_data.py` after `seed_stories.py` does **not** change the Story table row count. |
| 4 | All existing word and category seeding continues to function identically. |

## Testing Requirements

- Unit test: `seed_data.py` main function does not insert any Story rows.
- Integration test: sequential execution of `seed_data.py` then `seed_stories.py` produces exactly the expected story count with no duplicates.
- Existing word/category seeding tests must continue to pass.
- Test coverage ≥ 85%.
