"""Tests for user-contributed words (POST /api/dictionary/words)."""
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.models import Category, Word, WordCategory

from .conftest import TestSessionLocal as SessionLocal


def register_and_token(client: TestClient, email: str = "ugc@example.com", host_id: str = "marco") -> str:
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


def seed_category(cat_id: str = "cat-ugc") -> str:
    db = SessionLocal()
    db.add(Category(id=cat_id, name_en="Test", name_da="Test", name_it="Test", order=1))
    db.commit()
    db.close()
    return cat_id


# ---------- Success ----------


@patch("app.routers.dictionary.get_audio_path", return_value=None)
def test_create_word_success(mock_audio, client: TestClient) -> None:
    token = register_and_token(client)
    cat_id = seed_category()

    res = client.post(
        "/api/dictionary/words",
        json={
            "word": "gelato",
            "translation": "ice cream",
            "phoneticHint": "jeh-LAH-toh",
            "categoryId": cat_id,
            "difficulty": "beginner",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["word"] == "gelato"
    assert data["source"] == "user"
    assert data["language"] == "it"


@patch("app.routers.dictionary.get_audio_path", return_value=None)
def test_create_word_lowercased(mock_audio, client: TestClient) -> None:
    token = register_and_token(client, "ugclower@example.com")

    res = client.post(
        "/api/dictionary/words",
        json={"word": "CIAO", "translation": "hello"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    assert res.json()["word"] == "ciao"


@patch("app.routers.dictionary.get_audio_path", return_value=None)
def test_create_word_defaults_difficulty(mock_audio, client: TestClient) -> None:
    token = register_and_token(client, "ugcdiff@example.com")

    res = client.post(
        "/api/dictionary/words",
        json={"word": "grazie", "translation": "thanks"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200


@patch("app.routers.dictionary.get_audio_path", return_value=None)
def test_create_word_creates_uncategorised_category(mock_audio, client: TestClient) -> None:
    token = register_and_token(client, "ugcuncat@example.com")

    res = client.post(
        "/api/dictionary/words",
        json={"word": "prego", "translation": "you're welcome"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200

    # Verify uncategorised category was created
    db = SessionLocal()
    uncat = db.query(Category).filter(Category.id == "uncategorised").first()
    db.close()
    assert uncat is not None


# ---------- Validation ----------


def test_create_word_missing_word(client: TestClient) -> None:
    token = register_and_token(client, "ugcno1@example.com")

    res = client.post(
        "/api/dictionary/words",
        json={"translation": "something"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 400


def test_create_word_empty_word(client: TestClient) -> None:
    token = register_and_token(client, "ugcno2@example.com")

    res = client.post(
        "/api/dictionary/words",
        json={"word": "   ", "translation": "something"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 400


def test_create_word_missing_translation(client: TestClient) -> None:
    token = register_and_token(client, "ugcno3@example.com")

    res = client.post(
        "/api/dictionary/words",
        json={"word": "prova"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 400


def test_create_word_too_long(client: TestClient) -> None:
    token = register_and_token(client, "ugctoolong@example.com")

    res = client.post(
        "/api/dictionary/words",
        json={"word": "a" * 101, "translation": "too long"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 400


def test_create_word_no_letters(client: TestClient) -> None:
    token = register_and_token(client, "ugcnoletters@example.com")

    res = client.post(
        "/api/dictionary/words",
        json={"word": "12345", "translation": "numbers"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 400


def test_create_word_letters_with_digits(client: TestClient) -> None:
    token = register_and_token(client, "ugcdigits@example.com")

    res = client.post(
        "/api/dictionary/words",
        json={"word": "solskin3705", "translation": "sunshine"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 400


def test_create_word_invalid_difficulty(client: TestClient) -> None:
    token = register_and_token(client, "ugcinvdiff@example.com")

    res = client.post(
        "/api/dictionary/words",
        json={"word": "esempio", "translation": "example", "difficulty": "expert"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 400


def test_create_word_invalid_category(client: TestClient) -> None:
    token = register_and_token(client, "ugcinvcat@example.com")

    res = client.post(
        "/api/dictionary/words",
        json={"word": "scuola", "translation": "school", "categoryId": "nonexistent"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 400


# ---------- Duplicate detection ----------


@patch("app.routers.dictionary.get_audio_path", return_value=None)
def test_create_word_duplicate_returns_409(mock_audio, client: TestClient) -> None:
    token = register_and_token(client, "ugcdup@example.com")

    client.post(
        "/api/dictionary/words",
        json={"word": "duplicato", "translation": "duplicate"},
        headers={"Authorization": f"Bearer {token}"},
    )
    res = client.post(
        "/api/dictionary/words",
        json={"word": "duplicato", "translation": "duplicate again"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 409
    assert "existingWordId" in res.json()


def test_create_word_requires_auth(client: TestClient) -> None:
    res = client.post("/api/dictionary/words", json={"word": "test", "translation": "test"})
    assert res.status_code == 401


# ---------- Multi-translation ----------


@patch("app.routers.dictionary.get_audio_path", return_value=None)
def test_create_word_all_three_translations(mock_audio, client: TestClient) -> None:
    """When all three translationXx fields are provided, all columns are populated."""
    token = register_and_token(client, "ugcmulti1@example.com")

    res = client.post(
        "/api/dictionary/words",
        json={
            "word": "farfalla",
            "translationEn": "butterfly",
            "translationDa": "sommerfugl",
            "translationIt": "farfalla",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["translationEn"] == "butterfly"
    assert data["translationDa"] == "sommerfugl"
    assert data["translationIt"] == "farfalla"


@patch("app.routers.dictionary.get_audio_path", return_value=None)
def test_create_word_partial_translations(mock_audio, client: TestClient) -> None:
    """When only some translationXx fields are provided, missing ones are empty."""
    token = register_and_token(client, "ugcmulti2@example.com")

    res = client.post(
        "/api/dictionary/words",
        json={
            "word": "nuvola",
            "translationEn": "cloud",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["translationEn"] == "cloud"
    assert data["translationDa"] == ""
    assert data["translationIt"] == ""


@patch("app.routers.dictionary.get_audio_path", return_value=None)
def test_create_word_generic_translation_backward_compat(mock_audio, client: TestClient) -> None:
    """When only 'translation' is provided, it populates the contributor's ref lang column."""
    token = register_and_token(client, "ugcmulti3@example.com")  # language=en

    res = client.post(
        "/api/dictionary/words",
        json={"word": "sole", "translation": "sun"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    data = res.json()
    # Ref lang is "en" so translation should be in translationEn
    assert data["translationEn"] == "sun"
    assert data["translationDa"] == ""
    assert data["translationIt"] == ""


def test_create_word_no_translations_returns_400(client: TestClient) -> None:
    """When no translation fields are provided at all, returns 400."""
    token = register_and_token(client, "ugcmulti4@example.com")

    res = client.post(
        "/api/dictionary/words",
        json={"word": "vuoto"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 400
    assert "translation" in res.json()["error"].lower()


@patch("app.routers.dictionary.get_audio_path", return_value=None)
def test_create_word_explicit_overrides_generic(mock_audio, client: TestClient) -> None:
    """When both translationXx and translation are provided, explicit fields take precedence."""
    token = register_and_token(client, "ugcmulti5@example.com")  # language=en

    res = client.post(
        "/api/dictionary/words",
        json={
            "word": "luna",
            "translation": "moon",  # generic
            "translationEn": "moon",  # explicit
            "translationDa": "måne",  # explicit
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["translationEn"] == "moon"
    assert data["translationDa"] == "måne"
    assert data["translationIt"] == ""
