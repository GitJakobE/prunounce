from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.models import Word

from .conftest import TestSessionLocal as SessionLocal


def register_and_token(client: TestClient, email: str = "audio@example.com", host_id: str = "marco") -> str:
    res = client.post(
        "/api/auth/register",
        json={"email": email, "password": "Password1", "language": "en"},
    )
    assert res.status_code == 200
    token = res.json()["token"]
    client.patch(
        "/api/profile",
        json={"hostId": host_id},
        headers={"Authorization": f"Bearer {token}"},
    )
    return token


def seed_word(word: str = "ciao", language: str = "it", word_id: str = "w-ciao") -> str:
    db = SessionLocal()
    db.add(Word(
        id=word_id,
        word=word,
        language=language,
        phonetic_hint="chow",
        translation_en="hello",
        translation_da="hej",
        translation_it="ciao",
        difficulty="beginner",
        example_it="Ciao, come stai?",
        example_en="Hello, how are you?",
        example_da="Hej, hvordan har du det?",
        source="seed",
    ))
    db.commit()
    db.close()
    return word_id


# ---------- Word audio ----------


def test_audio_word_not_found(client: TestClient) -> None:
    token = register_and_token(client)
    res = client.get("/api/audio/missing-word", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 404
    assert res.json()["error"] == "Word not found"


def test_audio_language_mismatch(client: TestClient) -> None:
    """Italian host trying to get audio for Danish word should fail."""
    token = register_and_token(client, "audiolang@example.com", host_id="marco")
    seed_word(word="hej", language="da", word_id="w-hej-audio")

    res = client.get("/api/audio/w-hej-audio", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 400
    assert "language" in res.json()["error"].lower()


@patch("app.routers.audio.get_audio_path")
def test_audio_returns_file(mock_audio_path, client: TestClient, tmp_path: Path) -> None:
    token = register_and_token(client, "audiofile@example.com", host_id="marco")
    word_id = seed_word()

    fake_mp3 = tmp_path / "test.mp3"
    fake_mp3.write_bytes(b"\xff\xfb\x90\x00" + b"\x00" * 100)
    mock_audio_path.return_value = fake_mp3

    res = client.get(f"/api/audio/{word_id}", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.headers["content-type"] == "audio/mpeg"
    assert "max-age" in res.headers.get("cache-control", "")


@patch("app.routers.audio.get_audio_path")
def test_audio_returns_503_when_tts_fails(mock_audio_path, client: TestClient) -> None:
    token = register_and_token(client, "audio503@example.com", host_id="marco")
    word_id = seed_word()

    mock_audio_path.return_value = None
    res = client.get(f"/api/audio/{word_id}", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 503


def test_audio_requires_auth(client: TestClient) -> None:
    res = client.get("/api/audio/some-id")
    assert res.status_code == 401


# ---------- Example audio ----------


def test_audio_example_not_found(client: TestClient) -> None:
    token = register_and_token(client, "audioex@example.com")
    res = client.get("/api/audio/missing-word/example", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 404
    assert res.json()["error"] == "Example not found"


def test_audio_example_language_mismatch(client: TestClient) -> None:
    token = register_and_token(client, "audioexlang@example.com", host_id="marco")
    seed_word(word="hej", language="da", word_id="w-hej-ex")

    res = client.get("/api/audio/w-hej-ex/example", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 400


@patch("app.routers.audio.get_audio_path")
def test_audio_example_returns_file(mock_audio_path, client: TestClient, tmp_path: Path) -> None:
    token = register_and_token(client, "audioexfile@example.com", host_id="marco")
    word_id = seed_word()

    fake_mp3 = tmp_path / "example.mp3"
    fake_mp3.write_bytes(b"\xff\xfb\x90\x00" + b"\x00" * 100)
    mock_audio_path.return_value = fake_mp3

    res = client.get(f"/api/audio/{word_id}/example", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.headers["content-type"] == "audio/mpeg"


def test_audio_example_empty_text(client: TestClient) -> None:
    """Word with no example sentence should return 404."""
    token = register_and_token(client, "audionoex@example.com", host_id="marco")
    db = SessionLocal()
    db.add(Word(
        id="w-noexample",
        word="noexample",
        language="it",
        phonetic_hint="nope",
        translation_en="nope",
        translation_da="nope",
        translation_it="nope",
        difficulty="beginner",
        example_it="",
        example_en="",
        example_da="",
        source="seed",
    ))
    db.commit()
    db.close()

    res = client.get("/api/audio/w-noexample/example", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 404
