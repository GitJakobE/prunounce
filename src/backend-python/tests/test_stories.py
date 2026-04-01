"""Tests for the /api/stories endpoints (Task 029)."""

import json
import math

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import patch

from app.models import Story, StoryAudio, User
from app.services.story_audio import build_story_audio_bytes


# --- Helpers ---


def _make_user(db: Session, host_id: str = "marco", language: str = "it") -> User:
    user = User(
        email=f"stories-{host_id}@example.com",
        password_hash="x",
        language=language,
        host_id=host_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _make_story(
    db: Session,
    *,
    slug: str = "test-story",
    language: str = "it",
    difficulty: str = "beginner",
    length: str = "short",
    title: str = "Test",
    description_en: str = "An English description",
    description_da: str = "En dansk beskrivelse",
    description_it: str = "Una descrizione italiana",
    body: str = "Ciao mondo. " * 10,
    order: int = 0,
    format: str = "narrative",
    speakers: str | None = None,
) -> Story:
    story = Story(
        slug=slug,
        language=language,
        difficulty=difficulty,
        length=length,
        title=title,
        description_en=description_en,
        description_da=description_da,
        description_it=description_it,
        body=body,
        order=order,
        format=format,
        speakers=speakers,
    )
    db.add(story)
    db.commit()
    db.refresh(story)
    return story


def _register_and_token(client: TestClient, email: str, host_id: str = "marco") -> str:
    """Register a user, set their host, return JWT token."""
    res = client.post(
        "/api/auth/register",
        json={"email": email, "password": "Password1", "language": "en"},
    )
    assert res.status_code == 200, res.text
    token = res.json()["token"]
    client.patch(
        "/api/profile",
        json={"hostId": host_id},
        headers={"Authorization": f"Bearer {token}"},
    )
    return token


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _make_story_audio(
    db: Session,
    *,
    story_id: str,
    speed: str = "normal",
    audio_bytes: bytes = b"\xff\xfb\x90\x00" + b"\x00" * 64,
    content_hash: str = "hash",
) -> StoryAudio:
    story_audio = StoryAudio(
        story_id=story_id,
        speed=speed,
        mime_type="audio/mpeg",
        content_hash=content_hash,
        audio_bytes=audio_bytes,
    )
    db.add(story_audio)
    db.commit()
    db.refresh(story_audio)
    return story_audio


# --- Tests: GET /api/stories ---


class TestListStories:
    def test_requires_auth(self, client: TestClient) -> None:
        res = client.get("/api/stories")
        assert res.status_code == 401

    def test_returns_stories_grouped_by_difficulty(
        self, client: TestClient, clean_db: None
    ) -> None:
        from tests.conftest import TestSessionLocal

        db = TestSessionLocal()
        try:
            _make_story(db, slug="s1", language="it", difficulty="beginner", order=1)
            _make_story(db, slug="s2", language="it", difficulty="intermediate", order=1)
            _make_story(db, slug="s3", language="it", difficulty="advanced", order=1)
        finally:
            db.close()

        token = _register_and_token(client, "list@example.com", host_id="marco")
        res = client.get("/api/stories", headers=_auth(token))
        assert res.status_code == 200
        data = res.json()
        assert "stories" in data
        stories = data["stories"]
        assert "beginner" in stories
        assert "intermediate" in stories
        assert "advanced" in stories
        assert len(stories["beginner"]) == 1
        assert len(stories["intermediate"]) == 1
        assert len(stories["advanced"]) == 1
        assert stories["beginner"][0]["length"] == "short"

    def test_filters_by_target_language(
        self, client: TestClient, clean_db: None
    ) -> None:
        from tests.conftest import TestSessionLocal

        db = TestSessionLocal()
        try:
            _make_story(db, slug="it-story", language="it", difficulty="beginner")
            _make_story(db, slug="da-story", language="da", difficulty="beginner")
        finally:
            db.close()

        # marco is Italian host — should only see Italian stories
        token = _register_and_token(client, "filter@example.com", host_id="marco")
        res = client.get("/api/stories", headers=_auth(token))
        assert res.status_code == 200
        all_items = [
            item
            for group in res.json()["stories"].values()
            for item in group
        ]
        assert all(item["language"] == "it" for item in all_items)
        assert len(all_items) == 1

    def test_description_in_reference_language(
        self, client: TestClient, clean_db: None
    ) -> None:
        from tests.conftest import TestSessionLocal

        db = TestSessionLocal()
        try:
            _make_story(
                db,
                slug="desc-test",
                language="it",
                difficulty="beginner",
                description_en="English desc",
                description_da="Dansk beskrivelse",
            )
        finally:
            db.close()

        # Italian target → reference language is English (user registered with "en")
        token = _register_and_token(client, "refln@example.com", host_id="marco")
        res = client.get("/api/stories", headers=_auth(token))
        items = [i for g in res.json()["stories"].values() for i in g]
        assert items[0]["description"] == "English desc"

    def test_description_uses_user_reference_language_danish(
        self, client: TestClient, clean_db: None
    ) -> None:
        from tests.conftest import TestSessionLocal

        db = TestSessionLocal()
        try:
            _make_story(
                db,
                slug="desc-da",
                language="it",
                difficulty="beginner",
                description_en="English desc",
                description_da="Dansk beskrivelse",
                description_it="Descrizione italiana",
            )
        finally:
            db.close()

        # Register with Danish as reference language
        res = client.post(
            "/api/auth/register",
            json={"email": "ref-da@example.com", "password": "Password1", "language": "da"},
        )
        assert res.status_code == 200
        token = res.json()["token"]
        client.patch(
            "/api/profile",
            json={"hostId": "marco"},  # Italian host
            headers={"Authorization": f"Bearer {token}"},
        )

        res = client.get("/api/stories", headers={"Authorization": f"Bearer {token}"})
        items = [i for g in res.json()["stories"].values() for i in g]
        assert items[0]["description"] == "Dansk beskrivelse"

    def test_estimated_reading_time_computed(
        self, client: TestClient, clean_db: None
    ) -> None:
        from tests.conftest import TestSessionLocal

        # 150 words at 150 WPM → 1 minute
        body = " ".join(["parola"] * 150)
        db = TestSessionLocal()
        try:
            _make_story(db, slug="timing", language="it", difficulty="beginner", body=body)
        finally:
            db.close()

        token = _register_and_token(client, "time@example.com", host_id="marco")
        res = client.get("/api/stories", headers=_auth(token))
        items = [i for g in res.json()["stories"].values() for i in g]
        assert items[0]["estimatedReadingTime"] == 1

    def test_reading_time_rounds_up(
        self, client: TestClient, clean_db: None
    ) -> None:
        from tests.conftest import TestSessionLocal

        # 151 words → ceil(151/150) = 2
        body = " ".join(["parola"] * 151)
        db = TestSessionLocal()
        try:
            _make_story(db, slug="timing2", language="it", difficulty="beginner", body=body)
        finally:
            db.close()

        token = _register_and_token(client, "roundup@example.com", host_id="marco")
        res = client.get("/api/stories", headers=_auth(token))
        items = [i for g in res.json()["stories"].values() for i in g]
        assert items[0]["estimatedReadingTime"] == 2

    def test_stories_ordered_by_order_field(
        self, client: TestClient, clean_db: None
    ) -> None:
        from tests.conftest import TestSessionLocal

        db = TestSessionLocal()
        try:
            _make_story(db, slug="second", language="it", difficulty="beginner", title="Second", order=2)
            _make_story(db, slug="first", language="it", difficulty="beginner", title="First", order=1)
        finally:
            db.close()

        token = _register_and_token(client, "order@example.com", host_id="marco")
        res = client.get("/api/stories", headers=_auth(token))
        items = res.json()["stories"]["beginner"]
        assert items[0]["title"] == "First"
        assert items[1]["title"] == "Second"

    def test_empty_when_no_stories_for_language(
        self, client: TestClient, clean_db: None
    ) -> None:
        token = _register_and_token(client, "empty@example.com", host_id="marco")
        res = client.get("/api/stories", headers=_auth(token))
        assert res.status_code == 200
        stories = res.json()["stories"]
        assert all(len(v) == 0 for v in stories.values())

    def test_danish_host_sees_danish_stories(
        self, client: TestClient, clean_db: None
    ) -> None:
        from tests.conftest import TestSessionLocal

        db = TestSessionLocal()
        try:
            _make_story(db, slug="da-only", language="da", difficulty="beginner")
            _make_story(db, slug="it-only", language="it", difficulty="beginner")
        finally:
            db.close()

        # "freja" is a Danish host
        token = _register_and_token(client, "danish@example.com", host_id="freja")
        res = client.get("/api/stories", headers=_auth(token))
        all_items = [i for g in res.json()["stories"].values() for i in g]
        assert all(item["language"] == "da" for item in all_items)
        assert len(all_items) == 1


# --- Tests: GET /api/stories/:story_id ---


class TestGetStory:
    def test_requires_auth(self, client: TestClient) -> None:
        res = client.get("/api/stories/nonexistent")
        assert res.status_code == 401

    def test_returns_story_with_body(
        self, client: TestClient, clean_db: None
    ) -> None:
        from tests.conftest import TestSessionLocal

        db = TestSessionLocal()
        try:
            story = _make_story(
                db,
                slug="detail-test",
                language="it",
                difficulty="beginner",
                body="Il gatto è sul tavolo. " * 5,
            )
            story_id = story.id
        finally:
            db.close()

        token = _register_and_token(client, "detail@example.com", host_id="marco")
        res = client.get(f"/api/stories/{story_id}", headers=_auth(token))
        assert res.status_code == 200
        data = res.json()["story"]
        assert data["id"] == story_id
        assert "Il gatto è sul tavolo." in data["body"]
        assert data["slug"] == "detail-test"
        assert data["length"] == "short"

    def test_description_in_reference_language(
        self, client: TestClient, clean_db: None
    ) -> None:
        from tests.conftest import TestSessionLocal

        db = TestSessionLocal()
        try:
            story = _make_story(
                db,
                slug="ref-desc",
                language="it",
                difficulty="beginner",
                description_en="English detail",
                description_da="Dansk detalje",
            )
            story_id = story.id
        finally:
            db.close()

        token = _register_and_token(client, "refdetail@example.com", host_id="marco")
        res = client.get(f"/api/stories/{story_id}", headers=_auth(token))
        assert res.status_code == 200
        assert res.json()["story"]["description"] == "English detail"

    def test_detail_description_uses_user_reference_language_danish(
        self, client: TestClient, clean_db: None
    ) -> None:
        from tests.conftest import TestSessionLocal

        db = TestSessionLocal()
        try:
            story = _make_story(
                db,
                slug="ref-desc-da",
                language="it",
                difficulty="beginner",
                description_en="English detail",
                description_da="Dansk detalje",
                description_it="Dettaglio italiano",
            )
            story_id = story.id
        finally:
            db.close()

        # Register with Danish as reference language
        res = client.post(
            "/api/auth/register",
            json={"email": "detailref-da@example.com", "password": "Password1", "language": "da"},
        )
        assert res.status_code == 200
        token = res.json()["token"]
        client.patch(
            "/api/profile",
            json={"hostId": "marco"},
            headers={"Authorization": f"Bearer {token}"},
        )

        res = client.get(f"/api/stories/{story_id}", headers={"Authorization": f"Bearer {token}"})
        assert res.status_code == 200
        assert res.json()["story"]["description"] == "Dansk detalje"

    def test_404_for_nonexistent_story(
        self, client: TestClient, clean_db: None
    ) -> None:
        token = _register_and_token(client, "notfound@example.com", host_id="marco")
        res = client.get("/api/stories/does-not-exist", headers=_auth(token))
        assert res.status_code == 404

    def test_404_for_wrong_language_story(
        self, client: TestClient, clean_db: None
    ) -> None:
        from tests.conftest import TestSessionLocal

        db = TestSessionLocal()
        try:
            da_story = _make_story(db, slug="da-lang", language="da", difficulty="beginner")
            da_story_id = da_story.id
        finally:
            db.close()

        # Italian host cannot access a Danish story
        token = _register_and_token(client, "wronglang@example.com", host_id="marco")
        res = client.get(f"/api/stories/{da_story_id}", headers=_auth(token))
        assert res.status_code == 404

    def test_includes_estimated_reading_time(
        self, client: TestClient, clean_db: None
    ) -> None:
        from tests.conftest import TestSessionLocal

        body = " ".join(["parola"] * 300)  # ceil(300/150) = 2
        db = TestSessionLocal()
        try:
            story = _make_story(
                db, slug="timing3", language="it", difficulty="intermediate", body=body
            )
            story_id = story.id
        finally:
            db.close()

        token = _register_and_token(client, "detailtime@example.com", host_id="marco")
        res = client.get(f"/api/stories/{story_id}", headers=_auth(token))
        assert res.json()["story"]["estimatedReadingTime"] == 2


# --- Tests: dialogue metadata in API responses ---


class TestDialogueApiFields:
    """Verify that dialogue metadata (format, speakers, segments) appears in API responses."""

    def test_list_includes_format_and_speakers_for_dialogue(
        self, client: TestClient, clean_db: None
    ) -> None:
        from tests.conftest import TestSessionLocal

        db = TestSessionLocal()
        try:
            _make_story(
                db,
                slug="dlg-list",
                language="it",
                difficulty="beginner",
                body="Marco: Ciao!\nLucia: Ciao!",
                format="dialogue",
                speakers=json.dumps(["Marco", "Lucia"]),
            )
        finally:
            db.close()

        token = _register_and_token(client, "dlg-list@example.com", host_id="marco")
        res = client.get("/api/stories", headers=_auth(token))
        items = [i for g in res.json()["stories"].values() for i in g]
        assert len(items) == 1
        assert items[0]["format"] == "dialogue"
        assert items[0]["speakers"] == ["Marco", "Lucia"]

    def test_list_narrative_has_null_speakers(
        self, client: TestClient, clean_db: None
    ) -> None:
        from tests.conftest import TestSessionLocal

        db = TestSessionLocal()
        try:
            _make_story(
                db,
                slug="narr-list",
                language="it",
                difficulty="beginner",
                format="narrative",
            )
        finally:
            db.close()

        token = _register_and_token(client, "narr-list@example.com", host_id="marco")
        res = client.get("/api/stories", headers=_auth(token))
        items = [i for g in res.json()["stories"].values() for i in g]
        assert items[0]["format"] == "narrative"
        assert items[0]["speakers"] is None

    def test_detail_dialogue_returns_segments(
        self, client: TestClient, clean_db: None
    ) -> None:
        from tests.conftest import TestSessionLocal

        db = TestSessionLocal()
        try:
            story = _make_story(
                db,
                slug="dlg-detail",
                language="it",
                difficulty="beginner",
                body="Marco: Ciao!\nLucia: Buongiorno!",
                format="dialogue",
                speakers=json.dumps(["Marco", "Lucia"]),
            )
            story_id = story.id
        finally:
            db.close()

        token = _register_and_token(client, "dlg-detail@example.com", host_id="marco")
        res = client.get(f"/api/stories/{story_id}", headers=_auth(token))
        data = res.json()["story"]
        assert data["format"] == "dialogue"
        assert data["speakers"] == ["Marco", "Lucia"]
        assert len(data["segments"]) == 2
        assert data["segments"][0] == {"type": "dialogue", "speaker": "Marco", "text": "Ciao!"}
        assert data["segments"][1] == {"type": "dialogue", "speaker": "Lucia", "text": "Buongiorno!"}
        # raw body still present
        assert "Marco: Ciao!" in data["body"]

    def test_detail_narrative_returns_single_segment(
        self, client: TestClient, clean_db: None
    ) -> None:
        from tests.conftest import TestSessionLocal

        db = TestSessionLocal()
        try:
            story = _make_story(
                db,
                slug="narr-detail",
                language="it",
                difficulty="beginner",
                body="Il gatto dorme.",
                format="narrative",
            )
            story_id = story.id
        finally:
            db.close()

        token = _register_and_token(client, "narr-det@example.com", host_id="marco")
        res = client.get(f"/api/stories/{story_id}", headers=_auth(token))
        data = res.json()["story"]
        assert data["format"] == "narrative"
        assert data["speakers"] is None
        assert len(data["segments"]) == 1
        assert data["segments"][0] == {"type": "narration", "text": "Il gatto dorme."}

    def test_detail_mixed_returns_interleaved_segments(
        self, client: TestClient, clean_db: None
    ) -> None:
        from tests.conftest import TestSessionLocal

        db = TestSessionLocal()
        try:
            story = _make_story(
                db,
                slug="mix-detail",
                language="it",
                difficulty="intermediate",
                body="La porta si apre.\nMarco: Buongiorno!",
                format="mixed",
                speakers=json.dumps(["Marco"]),
            )
            story_id = story.id
        finally:
            db.close()

        token = _register_and_token(client, "mix-det@example.com", host_id="marco")
        res = client.get(f"/api/stories/{story_id}", headers=_auth(token))
        data = res.json()["story"]
        assert data["format"] == "mixed"
        assert len(data["segments"]) == 2
        assert data["segments"][0] == {"type": "narration", "text": "La porta si apre."}
        assert data["segments"][1] == {"type": "dialogue", "speaker": "Marco", "text": "Buongiorno!"}


class TestStoryAudio:
    def test_requires_auth(self, client: TestClient) -> None:
        res = client.get("/api/stories/some-story/audio")
        assert res.status_code == 401

    def test_returns_pre_generated_audio(self, client: TestClient, clean_db: None) -> None:
        from tests.conftest import TestSessionLocal

        db = TestSessionLocal()
        try:
            story = _make_story(db, slug="audio-story", language="it", difficulty="beginner")
            _make_story_audio(db, story_id=story.id, speed="normal")
            story_id = story.id
        finally:
            db.close()

        token = _register_and_token(client, "story-audio@example.com", host_id="marco")
        res = client.get(f"/api/stories/{story_id}/audio", headers=_auth(token))
        assert res.status_code == 200
        assert res.headers["content-type"] == "audio/mpeg"
        assert "immutable" in res.headers.get("cache-control", "")
        assert res.content.startswith(b"\xff\xfb")

    def test_returns_503_when_audio_not_pre_generated(self, client: TestClient, clean_db: None) -> None:
        from tests.conftest import TestSessionLocal

        db = TestSessionLocal()
        try:
            story = _make_story(db, slug="audio-missing", language="it", difficulty="beginner")
            story_id = story.id
        finally:
            db.close()

        token = _register_and_token(client, "story-audio-missing@example.com", host_id="marco")
        res = client.get(f"/api/stories/{story_id}/audio", headers=_auth(token))
        assert res.status_code == 503

    def test_returns_404_for_wrong_language_story_audio(self, client: TestClient, clean_db: None) -> None:
        from tests.conftest import TestSessionLocal

        db = TestSessionLocal()
        try:
            story = _make_story(db, slug="audio-da", language="da", difficulty="beginner")
            _make_story_audio(db, story_id=story.id, speed="normal")
            story_id = story.id
        finally:
            db.close()

        token = _register_and_token(client, "story-audio-wrong-lang@example.com", host_id="marco")
        res = client.get(f"/api/stories/{story_id}/audio", headers=_auth(token))
        assert res.status_code == 404


class TestStoryAudioGeneration:
    @patch("app.services.story_audio.PROVIDER.generate_bytes")
    def test_dialogue_audio_uses_text_without_speaker_labels(self, mock_generate_bytes) -> None:
        mock_generate_bytes.side_effect = [b"part1", b"part2"]
        story = Story(
            id="story-dialogue-1",
            slug="story-dialogue-1",
            language="it",
            difficulty="beginner",
            length="short",
            title="Dialogo",
            description_en="",
            description_da="",
            description_it="",
            body="Marco: Ciao!\nLucia: Buongiorno!",
            format="dialogue",
            speakers=json.dumps(["Marco", "Lucia"]),
            order=1,
        )

        audio = build_story_audio_bytes(story, "normal")

        assert audio == b"part1part2"
        assert mock_generate_bytes.call_args_list[0].args[0] == "Ciao!"
        assert mock_generate_bytes.call_args_list[1].args[0] == "Buongiorno!"

    @patch("app.services.story_audio.PROVIDER.generate_bytes")
    def test_dialogue_audio_switches_voice_between_speakers(self, mock_generate_bytes) -> None:
        mock_generate_bytes.side_effect = [b"one", b"two", b"three"]
        story = Story(
            id="story-dialogue-2",
            slug="story-dialogue-2",
            language="en",
            difficulty="beginner",
            length="short",
            title="Conversation",
            description_en="",
            description_da="",
            description_it="",
            body="Alex: Hello there.\nJordan: Hi Alex.\nAlex: Ready to begin?",
            format="dialogue",
            speakers=json.dumps(["Alex", "Jordan"]),
            order=1,
        )

        build_story_audio_bytes(story, "normal")

        assert mock_generate_bytes.call_args_list[0].args[1] != mock_generate_bytes.call_args_list[1].args[1]
        assert mock_generate_bytes.call_args_list[0].args[1] == mock_generate_bytes.call_args_list[2].args[1]
