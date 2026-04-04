# Story Seed Structure

- **Active seed file**: `src/backend-python/seed_stories.py`
- **Legacy JSON (old Node backend)**: `src/backend/data/stories.json` — used by `tests/test_story_seed.py` only
- **27 base stories** (9 per language × 3 difficulty tiers)
- Expanded to 81 stories via `_build_story_variants()` (short, medium, long per base)
- Each story has `setup_type` (6 pattern types) and `setup_summary` metadata
- Story model fields: `src/backend-python/app/models.py` lines 91-92
- Tests in `tests/test_stories.py` use inline `_make_story()` helpers, not seed data
- Poetry environment required for full test suite; `bcrypt<4.0.0` pinned in pyproject.toml
