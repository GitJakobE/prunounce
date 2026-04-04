"""Tests for the /api/reports endpoints (Task 048)."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import ContentReport, Story, User, Word


# --- Helpers ---


def _make_user(db: Session, email: str = "reporter@example.com") -> User:
    user = User(email=email, password_hash="x", language="en", host_id="marco")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _make_story(db: Session, *, slug: str = "test-story", language: str = "it") -> Story:
    story = Story(
        slug=slug,
        language=language,
        difficulty="beginner",
        title="Test Story",
        description_en="English",
        description_da="Dansk",
        description_it="Italiano",
        body="Ciao mondo. " * 10,
        order=0,
    )
    db.add(story)
    db.commit()
    db.refresh(story)
    return story


def _make_word(db: Session, *, word: str = "ciao", language: str = "it") -> Word:
    w = Word(
        word=word,
        language=language,
        phonetic_hint="chow",
        translation_en="hello",
        translation_da="hej",
        translation_it="ciao",
        difficulty="beginner",
    )
    db.add(w)
    db.commit()
    db.refresh(w)
    return w


def _register_and_token(client: TestClient, email: str = "reporter@example.com") -> str:
    res = client.post(
        "/api/auth/register",
        json={"email": email, "password": "Password1", "language": "en"},
    )
    assert res.status_code == 200, res.text
    token = res.json()["token"]
    client.patch(
        "/api/profile",
        json={"hostId": "marco"},
        headers={"Authorization": f"Bearer {token}"},
    )
    return token


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# --- Tests ---


class TestCreateReport:
    def test_create_report_for_story(self, client: TestClient, clean_db: None) -> None:
        from tests.conftest import TestSessionLocal

        db = TestSessionLocal()
        story = _make_story(db)
        db.close()

        token = _register_and_token(client)
        res = client.post(
            "/api/reports",
            json={
                "contentType": "story",
                "contentId": story.id,
                "category": "grammar_spelling",
                "description": "Spelling error in first paragraph",
            },
            headers=_auth(token),
        )
        assert res.status_code == 201
        data = res.json()
        assert data["contentType"] == "story"
        assert data["contentId"] == story.id
        assert data["category"] == "grammar_spelling"
        assert data["status"] == "new"
        assert data["description"] == "Spelling error in first paragraph"

    def test_create_report_for_word(self, client: TestClient, clean_db: None) -> None:
        from tests.conftest import TestSessionLocal

        db = TestSessionLocal()
        word = _make_word(db)
        db.close()

        token = _register_and_token(client)
        res = client.post(
            "/api/reports",
            json={
                "contentType": "word",
                "contentId": word.id,
                "category": "wrong_translation",
            },
            headers=_auth(token),
        )
        assert res.status_code == 201
        data = res.json()
        assert data["contentType"] == "word"
        assert data["contentId"] == word.id

    def test_duplicate_report_rejected(self, client: TestClient, clean_db: None) -> None:
        from tests.conftest import TestSessionLocal

        db = TestSessionLocal()
        story = _make_story(db)
        db.close()

        token = _register_and_token(client)
        payload = {
            "contentType": "story",
            "contentId": story.id,
            "category": "grammar_spelling",
        }
        res1 = client.post("/api/reports", json=payload, headers=_auth(token))
        assert res1.status_code == 201

        res2 = client.post("/api/reports", json=payload, headers=_auth(token))
        assert res2.status_code == 409

    def test_invalid_content_type(self, client: TestClient, clean_db: None) -> None:
        token = _register_and_token(client)
        res = client.post(
            "/api/reports",
            json={
                "contentType": "video",
                "contentId": "fake-id",
                "category": "other",
            },
            headers=_auth(token),
        )
        assert res.status_code == 422

    def test_nonexistent_content_id(self, client: TestClient, clean_db: None) -> None:
        token = _register_and_token(client)
        res = client.post(
            "/api/reports",
            json={
                "contentType": "story",
                "contentId": "nonexistent-id",
                "category": "other",
            },
            headers=_auth(token),
        )
        assert res.status_code == 404

    def test_description_too_long(self, client: TestClient, clean_db: None) -> None:
        from tests.conftest import TestSessionLocal

        db = TestSessionLocal()
        story = _make_story(db)
        db.close()

        token = _register_and_token(client)
        res = client.post(
            "/api/reports",
            json={
                "contentType": "story",
                "contentId": story.id,
                "category": "other",
                "description": "x" * 501,
            },
            headers=_auth(token),
        )
        assert res.status_code in (400, 422)

    def test_unauthenticated_rejected(self, client: TestClient, clean_db: None) -> None:
        res = client.post(
            "/api/reports",
            json={
                "contentType": "story",
                "contentId": "any",
                "category": "other",
            },
        )
        assert res.status_code == 401


class TestListReports:
    def test_list_all_reports(self, client: TestClient, clean_db: None) -> None:
        from tests.conftest import TestSessionLocal

        db = TestSessionLocal()
        story = _make_story(db)
        db.close()

        token = _register_and_token(client)
        client.post(
            "/api/reports",
            json={"contentType": "story", "contentId": story.id, "category": "grammar_spelling"},
            headers=_auth(token),
        )

        res = client.get("/api/reports", headers=_auth(token))
        assert res.status_code == 200
        data = res.json()
        assert data["total"] == 1
        assert len(data["items"]) == 1

    def test_filter_by_status(self, client: TestClient, clean_db: None) -> None:
        from tests.conftest import TestSessionLocal

        db = TestSessionLocal()
        story = _make_story(db)
        db.close()

        token = _register_and_token(client)
        client.post(
            "/api/reports",
            json={"contentType": "story", "contentId": story.id, "category": "grammar_spelling"},
            headers=_auth(token),
        )

        res = client.get("/api/reports?status=new", headers=_auth(token))
        assert res.status_code == 200
        assert res.json()["total"] == 1

        res = client.get("/api/reports?status=resolved", headers=_auth(token))
        assert res.status_code == 200
        assert res.json()["total"] == 0

    def test_filter_by_content_type(self, client: TestClient, clean_db: None) -> None:
        from tests.conftest import TestSessionLocal

        db = TestSessionLocal()
        story = _make_story(db)
        word = _make_word(db)
        story_id = story.id
        word_id = word.id
        db.close()

        token = _register_and_token(client)
        client.post(
            "/api/reports",
            json={"contentType": "story", "contentId": story_id, "category": "grammar_spelling"},
            headers=_auth(token),
        )
        client.post(
            "/api/reports",
            json={"contentType": "word", "contentId": word_id, "category": "wrong_translation"},
            headers=_auth(token),
        )

        res = client.get("/api/reports?content_type=story", headers=_auth(token))
        assert res.status_code == 200
        assert res.json()["total"] == 1
        assert res.json()["items"][0]["contentType"] == "story"

    def test_unauthenticated_rejected(self, client: TestClient, clean_db: None) -> None:
        res = client.get("/api/reports")
        assert res.status_code == 401


class TestUpdateReport:
    def test_update_status(self, client: TestClient, clean_db: None) -> None:
        from tests.conftest import TestSessionLocal

        db = TestSessionLocal()
        story = _make_story(db)
        db.close()

        token = _register_and_token(client)
        create_res = client.post(
            "/api/reports",
            json={"contentType": "story", "contentId": story.id, "category": "grammar_spelling"},
            headers=_auth(token),
        )
        report_id = create_res.json()["id"]

        res = client.patch(
            f"/api/reports/{report_id}",
            json={"status": "resolved", "resolutionNote": "Fixed the typo"},
            headers=_auth(token),
        )
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "resolved"
        assert data["resolutionNote"] == "Fixed the typo"

    def test_update_with_resolution_note(self, client: TestClient, clean_db: None) -> None:
        from tests.conftest import TestSessionLocal

        db = TestSessionLocal()
        story = _make_story(db)
        db.close()

        token = _register_and_token(client)
        create_res = client.post(
            "/api/reports",
            json={"contentType": "story", "contentId": story.id, "category": "other"},
            headers=_auth(token),
        )
        report_id = create_res.json()["id"]

        res = client.patch(
            f"/api/reports/{report_id}",
            json={"status": "dismissed", "resolutionNote": "Not a real issue"},
            headers=_auth(token),
        )
        assert res.status_code == 200
        assert res.json()["resolutionNote"] == "Not a real issue"

    def test_report_count_accuracy(self, client: TestClient, clean_db: None) -> None:
        """Multiple users reporting the same story → both appear in list."""
        from tests.conftest import TestSessionLocal

        db = TestSessionLocal()
        story = _make_story(db)
        db.close()

        token1 = _register_and_token(client, "user1@example.com")
        token2 = _register_and_token(client, "user2@example.com")

        client.post(
            "/api/reports",
            json={"contentType": "story", "contentId": story.id, "category": "grammar_spelling"},
            headers=_auth(token1),
        )
        client.post(
            "/api/reports",
            json={"contentType": "story", "contentId": story.id, "category": "wrong_translation"},
            headers=_auth(token2),
        )

        res = client.get("/api/reports", headers=_auth(token1))
        assert res.status_code == 200
        assert res.json()["total"] == 2

    def test_nonexistent_report(self, client: TestClient, clean_db: None) -> None:
        token = _register_and_token(client)
        res = client.patch(
            "/api/reports/nonexistent-id",
            json={"status": "resolved"},
            headers=_auth(token),
        )
        assert res.status_code == 404
