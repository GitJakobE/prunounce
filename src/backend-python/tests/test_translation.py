"""Tests for the translation service (Task 057) and lookup cascade (Task 058)."""

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.models import TranslationCache, Word
from app.services.translation import PROVIDER, translate_word

from .conftest import TestSessionLocal as SessionLocal


# ── Helpers ──────────────────────────────────────────────────────────────────


def _seed_word(
    *,
    word: str,
    language: str = "it",
    phonetic_hint: str = "hint",
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


def _seed_cache(*, word: str, source_lang: str, target_lang: str, translation: str) -> None:
    db = SessionLocal()
    db.add(
        TranslationCache(
            word=word,
            source_lang=source_lang,
            target_lang=target_lang,
            translation=translation,
        )
    )
    db.commit()
    db.close()


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


# ── TranslationCache model tests (Task 056) ─────────────────────────────────


class TestTranslationCacheModel:
    def test_insert_and_query(self) -> None:
        db = SessionLocal()
        entry = TranslationCache(
            word="ciao", source_lang="it", target_lang="en", translation="hello"
        )
        db.add(entry)
        db.commit()

        found = (
            db.query(TranslationCache)
            .filter(
                TranslationCache.word == "ciao",
                TranslationCache.source_lang == "it",
                TranslationCache.target_lang == "en",
            )
            .first()
        )
        assert found is not None
        assert found.translation == "hello"
        assert found.id is not None
        db.close()

    def test_unique_constraint(self) -> None:
        db = SessionLocal()
        db.add(TranslationCache(word="ciao", source_lang="it", target_lang="en", translation="hello"))
        db.commit()

        db.add(TranslationCache(word="ciao", source_lang="it", target_lang="en", translation="hi"))
        with pytest.raises(Exception):  # IntegrityError
            db.commit()
        db.rollback()
        db.close()

    def test_different_lang_pairs_allowed(self) -> None:
        db = SessionLocal()
        db.add(TranslationCache(word="ciao", source_lang="it", target_lang="en", translation="hello"))
        db.add(TranslationCache(word="ciao", source_lang="it", target_lang="da", translation="hej"))
        db.commit()

        count = db.query(TranslationCache).filter(TranslationCache.word == "ciao").count()
        assert count == 2
        db.close()


# ── Translation service tests (Task 057) ────────────────────────────────────


class TestTranslateWord:
    def test_cache_hit_returns_cached(self) -> None:
        _seed_cache(word="buongiorno", source_lang="it", target_lang="en", translation="good morning")
        db = SessionLocal()
        translation, source = translate_word("buongiorno", "it", "en", db)
        db.close()
        assert translation == "good morning"
        assert source == "cached"

    @patch.object(PROVIDER, "translate", return_value="goodbye")
    def test_cache_miss_calls_provider_and_caches(self, mock_translate) -> None:
        db = SessionLocal()
        translation, source = translate_word("arrivederci", "it", "en", db)
        assert translation == "goodbye"
        assert source == "auto-translated"
        mock_translate.assert_called_once_with("arrivederci", "it", "en")

        # Verify it was cached
        cached = (
            db.query(TranslationCache)
            .filter(
                TranslationCache.word == "arrivederci",
                TranslationCache.source_lang == "it",
                TranslationCache.target_lang == "en",
            )
            .first()
        )
        assert cached is not None
        assert cached.translation == "goodbye"
        db.close()

    @patch.object(PROVIDER, "translate", return_value=None)
    def test_provider_failure_returns_none(self, mock_translate) -> None:
        db = SessionLocal()
        translation, source = translate_word("sconosciuto", "it", "en", db)
        assert translation is None
        assert source == "none"

        # Not cached
        cached = (
            db.query(TranslationCache)
            .filter(TranslationCache.word == "sconosciuto")
            .first()
        )
        assert cached is None
        db.close()

    @patch.object(PROVIDER, "translate", return_value="hello")
    def test_cache_hit_skips_provider(self, mock_translate) -> None:
        _seed_cache(word="ciao", source_lang="it", target_lang="en", translation="hi")
        db = SessionLocal()
        translation, source = translate_word("ciao", "it", "en", db)
        db.close()
        assert translation == "hi"
        assert source == "cached"
        mock_translate.assert_not_called()

    def test_invalid_language_returns_none(self) -> None:
        db = SessionLocal()
        translation, source = translate_word("test", "xx", "en", db)
        db.close()
        assert translation is None
        assert source == "none"

    @patch.object(PROVIDER, "translate", return_value="Hej")
    def test_normalises_word_to_lowercase(self, mock_translate) -> None:
        db = SessionLocal()
        translate_word("CIAO", "it", "da", db)
        mock_translate.assert_called_once_with("ciao", "it", "da")
        db.close()


# ── Lookup cascade endpoint tests (Task 058) ─────────────────────────────────


class TestLookupCascade:
    def test_curated_word_returns_source_curated(self, client: TestClient) -> None:
        _seed_word(word="ciao", translation_en="hello")
        token = _register_and_token(client, "cascade-curated@example.com")

        res = client.get("/api/dictionary/lookup?word=ciao", headers=_auth(token))
        assert res.status_code == 200
        data = res.json()
        assert data["source"] == "curated"
        assert data["translation"] == "hello"
        assert data["wordId"] is not None

    @patch.object(PROVIDER, "translate", return_value=None)
    def test_not_found_with_failed_provider_returns_none(self, mock_translate, client: TestClient) -> None:
        token = _register_and_token(client, "cascade-none@example.com")

        res = client.get("/api/dictionary/lookup?word=sconosciuto", headers=_auth(token))
        assert res.status_code == 200
        data = res.json()
        assert data["source"] == "none"
        assert data["translation"] is None
        assert data["wordId"] is None

    def test_cached_translation_returns_source_cached(self, client: TestClient) -> None:
        _seed_cache(word="buongiorno", source_lang="it", target_lang="en", translation="good morning")
        token = _register_and_token(client, "cascade-cached@example.com")

        res = client.get("/api/dictionary/lookup?word=buongiorno", headers=_auth(token))
        assert res.status_code == 200
        data = res.json()
        assert data["source"] == "cached"
        assert data["translation"] == "good morning"
        assert data["wordId"] is None

    @patch.object(PROVIDER, "translate", return_value="goodbye")
    def test_auto_translated_returns_source_auto(self, mock_translate, client: TestClient) -> None:
        token = _register_and_token(client, "cascade-auto@example.com")

        res = client.get("/api/dictionary/lookup?word=arrivederci", headers=_auth(token))
        assert res.status_code == 200
        data = res.json()
        assert data["source"] == "auto-translated"
        assert data["translation"] == "goodbye"
        assert data["wordId"] is None

    @patch.object(PROVIDER, "translate", return_value="goodbye")
    def test_auto_translated_then_cached(self, mock_translate, client: TestClient) -> None:
        token = _register_and_token(client, "cascade-then-cache@example.com")

        # First call: auto-translated
        res1 = client.get("/api/dictionary/lookup?word=arrivederci", headers=_auth(token))
        assert res1.json()["source"] == "auto-translated"
        mock_translate.assert_called_once()

        mock_translate.reset_mock()

        # Second call: should come from cache
        res2 = client.get("/api/dictionary/lookup?word=arrivederci", headers=_auth(token))
        assert res2.json()["source"] == "cached"
        assert res2.json()["translation"] == "goodbye"
        mock_translate.assert_not_called()

    def test_curated_takes_priority_over_cache(self, client: TestClient) -> None:
        _seed_word(word="grazie", translation_en="thanks")
        _seed_cache(word="grazie", source_lang="it", target_lang="en", translation="thank you (cached)")
        token = _register_and_token(client, "cascade-priority@example.com")

        res = client.get("/api/dictionary/lookup?word=grazie", headers=_auth(token))
        assert res.status_code == 200
        data = res.json()
        assert data["source"] == "curated"
        assert data["translation"] == "thanks"
