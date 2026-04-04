"""Tests for Task 030: Story seed data — seeder correctness and JSON data validation."""

import json
import re
from pathlib import Path

import pytest
from sqlalchemy.orm import Session

from app.models import Story

# Path to the seed JSON file
STORIES_JSON = (
    Path(__file__).parent.parent.parent / "backend" / "data" / "stories.json"
)

VALID_LANGUAGES = {"it", "da", "en", "es"}
VALID_DIFFICULTIES = {"beginner", "intermediate", "advanced"}
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

WORD_COUNT_RANGES = {
    "beginner": (50, 100),
    "intermediate": (150, 250),
    "advanced": (300, 500),
}


def word_count(text: str) -> int:
    return len(text.split())


def load_stories() -> list[dict]:
    with open(STORIES_JSON, encoding="utf-8") as f:
        return json.load(f)


# ------------------------------------------------------------------ JSON validation


class TestStoriesJsonStructure:
    """Validate the stories.json file itself without touching the database."""

    def test_json_file_exists(self) -> None:
        assert STORIES_JSON.exists(), f"stories.json not found at {STORIES_JSON}"

    def test_exactly_36_stories(self) -> None:
        stories = load_stories()
        assert len(stories) == 36, f"Expected 36 stories, got {len(stories)}"

    def test_nine_stories_per_language(self) -> None:
        stories = load_stories()
        by_lang: dict[str, int] = {}
        for s in stories:
            by_lang[s["language"]] = by_lang.get(s["language"], 0) + 1
        for lang in VALID_LANGUAGES:
            assert by_lang.get(lang, 0) == 9, (
                f"Expected 9 stories for language '{lang}', got {by_lang.get(lang, 0)}"
            )

    def test_three_stories_per_difficulty_per_language(self) -> None:
        stories = load_stories()
        counts: dict[tuple[str, str], int] = {}
        for s in stories:
            key = (s["language"], s["difficulty"])
            counts[key] = counts.get(key, 0) + 1
        for lang in VALID_LANGUAGES:
            for diff in VALID_DIFFICULTIES:
                assert counts.get((lang, diff), 0) == 3, (
                    f"Expected 3 stories for ({lang}, {diff}), got {counts.get((lang, diff), 0)}"
                )

    def test_all_required_fields_present(self) -> None:
        required = {"id", "slug", "language", "difficulty", "title",
                    "descriptionEn", "descriptionDa", "descriptionIt", "descriptionEs", "body", "order"}
        stories = load_stories()
        for s in stories:
            missing = required - set(s.keys())
            assert not missing, f"Story '{s.get('slug')}' is missing fields: {missing}"

    def test_valid_language_codes(self) -> None:
        stories = load_stories()
        for s in stories:
            assert s["language"] in VALID_LANGUAGES, (
                f"Story '{s['slug']}' has invalid language '{s['language']}'"
            )

    def test_valid_difficulty_levels(self) -> None:
        stories = load_stories()
        for s in stories:
            assert s["difficulty"] in VALID_DIFFICULTIES, (
                f"Story '{s['slug']}' has invalid difficulty '{s['difficulty']}'"
            )

    def test_slugs_are_url_friendly(self) -> None:
        stories = load_stories()
        for s in stories:
            assert SLUG_PATTERN.match(s["slug"]), (
                f"Slug '{s['slug']}' is not URL-friendly (must be lowercase, hyphens only)"
            )

    def test_slug_language_pairs_are_unique(self) -> None:
        stories = load_stories()
        seen: set[tuple[str, str]] = set()
        for s in stories:
            key = (s["slug"], s["language"])
            assert key not in seen, f"Duplicate (slug, language) pair: {key}"
            seen.add(key)

    def test_beginner_stories_word_count(self) -> None:
        stories = load_stories()
        lo, hi = WORD_COUNT_RANGES["beginner"]
        for s in [s for s in stories if s["difficulty"] == "beginner"]:
            count = word_count(s["body"])
            assert lo <= count <= hi, (
                f"Beginner story '{s['slug']}' has {count} words (expected {lo}–{hi})"
            )

    def test_intermediate_stories_word_count(self) -> None:
        stories = load_stories()
        lo, hi = WORD_COUNT_RANGES["intermediate"]
        for s in [s for s in stories if s["difficulty"] == "intermediate"]:
            count = word_count(s["body"])
            assert lo <= count <= hi, (
                f"Intermediate story '{s['slug']}' has {count} words (expected {lo}–{hi})"
            )

    def test_advanced_stories_word_count(self) -> None:
        stories = load_stories()
        lo, hi = WORD_COUNT_RANGES["advanced"]
        for s in [s for s in stories if s["difficulty"] == "advanced"]:
            count = word_count(s["body"])
            assert lo <= count <= hi, (
                f"Advanced story '{s['slug']}' has {count} words (expected {lo}–{hi})"
            )

    def test_descriptions_are_non_empty(self) -> None:
        stories = load_stories()
        for s in stories:
            for field in ("descriptionEn", "descriptionDa", "descriptionIt", "descriptionEs"):
                assert s[field].strip(), (
                    f"Story '{s['slug']}' has empty {field}"
                )

    def test_titles_are_non_empty(self) -> None:
        stories = load_stories()
        for s in stories:
            assert s["title"].strip(), f"Story '{s['slug']}' has an empty title"

    def test_all_ids_are_unique(self) -> None:
        stories = load_stories()
        ids = [s["id"] for s in stories]
        assert len(ids) == len(set(ids)), "Duplicate IDs found in stories.json"


# ------------------------------------------------------------------ Seeder integration


class TestSeedStories:
    """Test that seed_stories() inserts and upserts correctly."""

    def test_seeder_creates_all_stories(self, clean_db: None) -> None:
        from tests.conftest import TestSessionLocal
        from seed_data import seed_stories

        stories = load_stories()
        db = TestSessionLocal()
        try:
            seed_stories(db, stories)
            count = db.query(Story).count()
        finally:
            db.close()
        assert count == 36

    def test_seeder_is_idempotent(self, clean_db: None) -> None:
        from tests.conftest import TestSessionLocal
        from seed_data import seed_stories

        stories = load_stories()
        db = TestSessionLocal()
        try:
            seed_stories(db, stories)
            seed_stories(db, stories)  # run twice
            count = db.query(Story).count()
        finally:
            db.close()
        assert count == 36, "Re-running seeder should not create duplicates"

    def test_seeder_updates_existing_story_on_rerun(self, clean_db: None) -> None:
        from tests.conftest import TestSessionLocal
        from seed_data import seed_stories

        stories = load_stories()
        db = TestSessionLocal()
        try:
            seed_stories(db, stories)

            # Modify and re-seed one story
            modified = [
                {**s, "title": "Updated Title"} if s["slug"] == "al-caffe" and s["language"] == "it" else s
                for s in stories
            ]
            seed_stories(db, modified)

            updated = (
                db.query(Story)
                .filter(Story.slug == "al-caffe", Story.language == "it")
                .first()
            )
            assert updated is not None
            assert updated.title == "Updated Title"
        finally:
            db.close()

    def test_seeder_creates_stories_for_all_languages(self, clean_db: None) -> None:
        from tests.conftest import TestSessionLocal
        from seed_data import seed_stories

        db = TestSessionLocal()
        try:
            seed_stories(db, load_stories())
            for lang in VALID_LANGUAGES:
                count = db.query(Story).filter(Story.language == lang).count()
                assert count == 9, f"Expected 9 stories for '{lang}', got {count}"
        finally:
            db.close()

    def test_seeder_creates_all_difficulties(self, clean_db: None) -> None:
        from tests.conftest import TestSessionLocal
        from seed_data import seed_stories

        db = TestSessionLocal()
        try:
            seed_stories(db, load_stories())
            for diff in VALID_DIFFICULTIES:
                count = db.query(Story).filter(Story.difficulty == diff).count()
                assert count == 12, f"Expected 12 stories for difficulty '{diff}', got {count}"
        finally:
            db.close()
