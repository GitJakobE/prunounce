"""Tests for GET /api/dictionary/lookup (Task 029 – word lookup endpoint)."""

import pytest
from fastapi.testclient import TestClient

from app.models import Word

from .conftest import TestSessionLocal as SessionLocal


def _seed_word(
    *,
    word: str,
    language: str = "it",
    phonetic_hint: str = "test-hint",
    translation_en: str = "hello",
    translation_da: str = "hej",
    translation_it: str = "ciao",
    difficulty: str = "beginner",
) -> str:
    db = SessionLocal()
    w = Word(
        word=word,
        language=language,
        phonetic_hint=phonetic_hint,
        translation_en=translation_en,
        translation_da=translation_da,
        translation_it=translation_it,
        difficulty=difficulty,
        source="seed",
    )
    db.add(w)
    db.commit()
    db.refresh(w)
    word_id = w.id
    db.close()
    return word_id


def _register_and_token(client: TestClient, email: str, host_id: str = "marco") -> str:
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


class TestWordLookup:
    def test_requires_auth(self, client: TestClient) -> None:
        res = client.get("/api/dictionary/lookup?word=ciao")
        assert res.status_code == 401

    def test_found_exact_match(self, client: TestClient, clean_db: None) -> None:
        word_id = _seed_word(word="ciao", translation_en="hello")
        token = _register_and_token(client, "lookup-found@example.com", host_id="marco")

        res = client.get("/api/dictionary/lookup?word=ciao", headers=_auth(token))
        assert res.status_code == 200
        data = res.json()
        assert data["word"] == "ciao"
        assert data["translation"] == "hello"  # reference lang is English for Italian host
        assert data["wordId"] == word_id
        assert data["phoneticHint"] == "test-hint"

    def test_case_insensitive_match(self, client: TestClient, clean_db: None) -> None:
        _seed_word(word="ciao")
        token = _register_and_token(client, "lookup-case@example.com", host_id="marco")

        res = client.get("/api/dictionary/lookup?word=CIAO", headers=_auth(token))
        assert res.status_code == 200
        assert res.json()["word"] == "ciao"

    def test_diacritical_normalised_match(self, client: TestClient, clean_db: None) -> None:
        _seed_word(word="città")
        token = _register_and_token(client, "lookup-diac@example.com", host_id="marco")

        # Query without accent should still match
        res = client.get("/api/dictionary/lookup?word=citta", headers=_auth(token))
        assert res.status_code == 200
        assert res.json()["word"] == "città"

    def test_not_found_returns_null_fields(self, client: TestClient, clean_db: None) -> None:
        token = _register_and_token(client, "lookup-notfound@example.com", host_id="marco")

        res = client.get("/api/dictionary/lookup?word=zzznonsenseword", headers=_auth(token))
        assert res.status_code == 200
        data = res.json()
        assert data["translation"] is None
        assert data["phoneticHint"] is None
        assert data["wordId"] is None

    def test_language_filter_by_host(self, client: TestClient, clean_db: None) -> None:
        # Danish word must NOT be returned for an Italian host
        _seed_word(word="hej", language="da", translation_en="hello")
        _seed_word(word="ciao", language="it", translation_en="hello")

        token = _register_and_token(client, "lookup-lang@example.com", host_id="marco")  # Italian host

        res = client.get("/api/dictionary/lookup?word=hej", headers=_auth(token))
        assert res.status_code == 200
        # Should not find the Danish word for an Italian-language user
        assert res.json()["wordId"] is None

    def test_missing_word_query_param(self, client: TestClient) -> None:
        token = _register_and_token(client, "lookup-missing@example.com")
        res = client.get("/api/dictionary/lookup", headers=_auth(token))
        assert res.status_code in (400, 422)  # FastAPI validation error

    def test_lookup_returns_translation_in_user_reference_language_danish(
        self, client: TestClient, clean_db: None
    ) -> None:
        """User with reference language=da should see Danish translation."""
        _seed_word(
            word="ciao",
            language="it",
            translation_en="hello",
            translation_da="hej",
            translation_it="ciao",
        )
        # Register with Danish as reference language
        res = client.post(
            "/api/auth/register",
            json={"email": "reflang-da@example.com", "password": "Password1", "language": "da"},
        )
        assert res.status_code == 200
        token = res.json()["token"]
        client.patch(
            "/api/profile",
            json={"hostId": "marco"},  # Italian host
            headers=_auth(token),
        )

        res = client.get("/api/dictionary/lookup?word=ciao", headers=_auth(token))
        assert res.status_code == 200
        assert res.json()["translation"] == "hej"  # Danish, not English

    def test_lookup_returns_translation_in_user_reference_language_italian(
        self, client: TestClient, clean_db: None
    ) -> None:
        """User with reference language=it learning Danish should see Italian translation."""
        _seed_word(
            word="hej",
            language="da",
            translation_en="hello",
            translation_da="hej",
            translation_it="ciao",
        )
        res = client.post(
            "/api/auth/register",
            json={"email": "reflang-it@example.com", "password": "Password1", "language": "it"},
        )
        assert res.status_code == 200
        token = res.json()["token"]
        client.patch(
            "/api/profile",
            json={"hostId": "freja"},  # Danish host
            headers=_auth(token),
        )

        res = client.get("/api/dictionary/lookup?word=hej", headers=_auth(token))
        assert res.status_code == 200
        assert res.json()["translation"] == "ciao"  # Italian, not English

    def test_lookup_explicit_lang_param_overrides_profile(
        self, client: TestClient, clean_db: None
    ) -> None:
        """Explicit lang query param should override the user's stored preference."""
        _seed_word(
            word="ciao",
            language="it",
            translation_en="hello",
            translation_da="hej",
            translation_it="ciao",
        )
        # User has reference language=da
        res = client.post(
            "/api/auth/register",
            json={"email": "reflang-override@example.com", "password": "Password1", "language": "da"},
        )
        assert res.status_code == 200
        token = res.json()["token"]
        client.patch(
            "/api/profile",
            json={"hostId": "marco"},
            headers=_auth(token),
        )

        # But explicitly request English translation
        res = client.get("/api/dictionary/lookup?word=ciao&lang=en", headers=_auth(token))
        assert res.status_code == 200
        assert res.json()["translation"] == "hello"  # Explicit param wins
