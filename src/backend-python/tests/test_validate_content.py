"""Tests for validate_content.py (Task 047)."""

import json

import pytest
from sqlalchemy.orm import Session

from app.models import Story, Word


def _make_story(
    db: Session,
    *,
    slug: str = "test-story",
    language: str = "it",
    difficulty: str = "beginner",
    title: str = "Test",
    body: str = "Cliente: Ciao come stai oggi amico mio caro. " * 6,
    format: str = "dialogue",
    speakers: str | None = json.dumps(["Cliente", "Barista"]),
    order: int = 0,
) -> Story:
    story = Story(
        slug=slug,
        language=language,
        difficulty=difficulty,
        title=title,
        description_en="English",
        description_da="Dansk",
        description_it="Italiano",
        body=body,
        format=format,
        speakers=speakers,
        order=order,
    )
    db.add(story)
    db.commit()
    db.refresh(story)
    return story


class TestStoryValidation:
    def test_detects_low_word_count(self, clean_db: None) -> None:
        from tests.conftest import TestSessionLocal
        from validate_content import validate_stories

        db = TestSessionLocal()
        try:
            _make_story(db, slug="short-story", body="Cliente: Ciao.\nBarista: Ciao.", difficulty="beginner")
            issues = validate_stories(db)
            errors = [i for i in issues if i.level == "ERROR" and "word count" in i.message]
            assert len(errors) >= 1
        finally:
            db.close()

    def test_detects_bad_slug(self, clean_db: None) -> None:
        from tests.conftest import TestSessionLocal
        from validate_content import validate_stories

        db = TestSessionLocal()
        try:
            _make_story(db, slug="BAD_SLUG!", body="Cliente: " + " ".join(["parola"] * 60) + "\nBarista: Ciao.")
            issues = validate_stories(db)
            errors = [i for i in issues if i.level == "ERROR" and "slug" in i.message]
            assert len(errors) >= 1
        finally:
            db.close()

    def test_detects_empty_description(self, clean_db: None) -> None:
        from tests.conftest import TestSessionLocal
        from validate_content import validate_stories

        db = TestSessionLocal()
        try:
            s = _make_story(db, slug="empty-desc", body="Cliente: " + " ".join(["parola"] * 60) + "\nBarista: Ciao.")
            s.description_da = ""
            db.commit()
            issues = validate_stories(db)
            errors = [i for i in issues if i.level == "ERROR" and "description_da" in i.message]
            assert len(errors) >= 1
        finally:
            db.close()

    def test_detects_dialogue_speaker_mismatch(self, clean_db: None) -> None:
        from tests.conftest import TestSessionLocal
        from validate_content import validate_stories

        db = TestSessionLocal()
        try:
            _make_story(
                db,
                slug="bad-speakers",
                body="Marco: " + " ".join(["ciao"] * 30) + "\nLucia: " + " ".join(["ciao"] * 30),
                format="dialogue",
                speakers=json.dumps(["Marco", "Unknown"]),
            )
            issues = validate_stories(db)
            errors = [i for i in issues if i.level == "ERROR"]
            assert any("Lucia" in e.message for e in errors)
        finally:
            db.close()

    def test_clean_story_no_errors(self, clean_db: None) -> None:
        from tests.conftest import TestSessionLocal
        from validate_content import validate_stories

        db = TestSessionLocal()
        try:
            body = "\n".join(
                [f"Cliente: " + " ".join(["parola"] * 10)]
                + [f"Barista: " + " ".join(["parola"] * 10)]
                + [f"Cliente: " + " ".join(["parola"] * 10)]
                + [f"Barista: " + " ".join(["parola"] * 10)]
                + [f"Cliente: " + " ".join(["parola"] * 10)]
                + [f"Barista: " + " ".join(["parola"] * 10)]
            )
            _make_story(
                db,
                slug="clean-story",
                body=body,
                format="dialogue",
                speakers=json.dumps(["Cliente", "Barista"]),
                difficulty="beginner",
            )
            issues = validate_stories(db)
            errors = [i for i in issues if i.level == "ERROR"]
            assert len(errors) == 0
        finally:
            db.close()

    def test_language_filter(self, clean_db: None) -> None:
        from tests.conftest import TestSessionLocal
        from validate_content import validate_stories

        db = TestSessionLocal()
        try:
            body = "\n".join([f"Cliente: " + " ".join(["parola"] * 15) for _ in range(5)])
            _make_story(db, slug="it-test", language="it", body=body, speakers=json.dumps(["Cliente", "Barista"]))
            _make_story(db, slug="da-test", language="da", body="Kunde: " + " ".join(["ord"] * 5) + "\nBarista: hej.",
                        speakers=json.dumps(["Kunde", "Barista"]))
            # Only validate Italian — should not see Danish issues
            issues = validate_stories(db, language="it")
            assert all("da-test" not in i.target for i in issues)
        finally:
            db.close()


class TestWordValidation:
    def test_detects_missing_translation(self, clean_db: None) -> None:
        from tests.conftest import TestSessionLocal
        from validate_content import validate_words

        db = TestSessionLocal()
        try:
            w = Word(word="ciao", language="it", phonetic_hint="chow",
                     difficulty="beginner",
                     translation_en="hello", translation_da="", translation_it="ciao")
            db.add(w)
            db.commit()
            issues = validate_words(db)
            errors = [i for i in issues if i.level in ("ERROR", "WARNING") and "translation_da" in i.message]
            assert len(errors) >= 1
        finally:
            db.close()

    def test_detects_near_duplicates(self, clean_db: None) -> None:
        from tests.conftest import TestSessionLocal
        from validate_content import validate_words

        db = TestSessionLocal()
        try:
            db.add(Word(word="ciao", language="it", phonetic_hint="chow",
                        difficulty="beginner",
                        translation_en="hi", translation_da="hej", translation_it="ciao"))
            db.add(Word(word="ciap", language="it", phonetic_hint="chap",
                        difficulty="beginner",
                        translation_en="hi", translation_da="hej", translation_it="ciap"))
            db.commit()
            issues = validate_words(db)
            warnings = [i for i in issues if i.level == "WARNING" and "duplicate" in i.message]
            assert len(warnings) >= 1
        finally:
            db.close()


class TestJsonOutput:
    def test_json_report_is_valid(self, clean_db: None) -> None:
        from validate_content import _json_report, Issue

        story_issues = [Issue("ERROR", "story", "test-slug", "test error")]
        word_issues = [Issue("WARNING", "word", "test-word", "test warning")]
        output = _json_report(story_issues, word_issues)
        data = json.loads(output)
        assert data["summary"]["status"] == "FAIL"
        assert data["summary"]["story_errors"] == 1
        assert data["summary"]["word_warnings"] == 1
        assert len(data["stories"]) == 1
        assert len(data["words"]) == 1


class TestEditDistance:
    def test_identical_strings(self) -> None:
        from validate_content import _edit_distance
        assert _edit_distance("hello", "hello") == 0

    def test_single_edit(self) -> None:
        from validate_content import _edit_distance
        assert _edit_distance("hello", "helo") == 1

    def test_empty_string(self) -> None:
        from validate_content import _edit_distance
        assert _edit_distance("abc", "") == 3
