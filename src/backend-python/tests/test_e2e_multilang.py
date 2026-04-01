"""End-to-end multi-language and user-contributed-words integration tests (Task 028)."""
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.models import Category, Word, WordCategory, UserProgress

from .conftest import TestSessionLocal as SessionLocal


def _register(client: TestClient, email: str, host_id: str = "marco") -> str:
    res = client.post(
        "/api/auth/register",
        json={"email": email, "password": "Password1", "language": "en"},
    )
    assert res.status_code == 200
    token = res.json()["token"]
    client.patch("/api/profile", json={"hostId": host_id}, headers={"Authorization": f"Bearer {token}"})
    return token


def _seed_multilang() -> None:
    """Seed one category with Italian, Danish, and English words."""
    db = SessionLocal()
    cat = Category(id="cat-greet", name_en="Greetings", name_da="Hilsner", name_it="Saluti", order=1)
    db.add(cat)

    words = [
        Word(id="w-ciao", word="ciao", language="it", phonetic_hint="chow", translation_en="hello",
             translation_da="hej", translation_it="ciao", difficulty="beginner",
             example_it="Ciao, come stai?", example_en="Hello, how are you?", example_da="Hej, hvordan har du det?", source="seed"),
        Word(id="w-hej", word="hej", language="da", phonetic_hint="hai", translation_en="hello",
             translation_da="hej", translation_it="ciao", difficulty="beginner",
             example_it="Ciao!", example_en="Hello!", example_da="Hej!", source="seed"),
        Word(id="w-hello", word="hello", language="en", phonetic_hint="heh-LOH", translation_en="hello",
             translation_da="hej", translation_it="ciao", difficulty="beginner",
             example_it="Ciao!", example_en="Hello!", example_da="Hej!", source="seed"),
    ]
    for w in words:
        db.add(w)
    db.flush()
    for w in words:
        db.add(WordCategory(word_id=w.id, category_id=cat.id))
    db.commit()
    db.close()


# ---------- Host switching changes dictionary ----------


def test_host_switch_changes_words(client: TestClient) -> None:
    """Switching from Italian to Danish host changes which words are returned."""
    token = _register(client, "e2e_switch@example.com", host_id="marco")
    _seed_multilang()

    # Italian host → Italian words
    res_it = client.get("/api/dictionary/categories/cat-greet/words", headers={"Authorization": f"Bearer {token}"})
    assert res_it.status_code == 200
    words_it = res_it.json()["words"]
    assert len(words_it) == 1
    assert words_it[0]["word"] == "ciao"

    # Switch to Danish host
    client.patch("/api/profile", json={"hostId": "anders"}, headers={"Authorization": f"Bearer {token}"})

    res_da = client.get("/api/dictionary/categories/cat-greet/words", headers={"Authorization": f"Bearer {token}"})
    words_da = res_da.json()["words"]
    assert len(words_da) == 1
    assert words_da[0]["word"] == "hej"

    # Switch to English host
    client.patch("/api/profile", json={"hostId": "james"}, headers={"Authorization": f"Bearer {token}"})

    res_en = client.get("/api/dictionary/categories/cat-greet/words", headers={"Authorization": f"Bearer {token}"})
    words_en = res_en.json()["words"]
    assert len(words_en) == 1
    assert words_en[0]["word"] == "hello"


# ---------- Search scoped to target language ----------


def test_search_scoped_to_target_language(client: TestClient) -> None:
    """Search only returns words in the target language, not others."""
    token = _register(client, "e2e_search@example.com", host_id="marco")
    _seed_multilang()

    # Italian host: search for "hello" should match via translation, not the English word
    res = client.get("/api/search?q=ciao", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    results = res.json()["results"]
    assert all(r["word"] != "hello" for r in results)

    # Switch to English host
    client.patch("/api/profile", json={"hostId": "james"}, headers={"Authorization": f"Bearer {token}"})

    res_en = client.get("/api/search?q=hello", headers={"Authorization": f"Bearer {token}"})
    results_en = res_en.json()["results"]
    assert len(results_en) >= 1
    assert results_en[0]["word"] == "hello"


# ---------- Progress isolation across languages ----------


def test_progress_isolation_across_languages(client: TestClient) -> None:
    """Progress in Italian doesn't show when user switches to Danish."""
    token = _register(client, "e2e_progress@example.com", host_id="marco")
    _seed_multilang()

    # Listen to Italian word
    client.post("/api/dictionary/words/w-ciao/listened", headers={"Authorization": f"Bearer {token}"})

    # Italian progress: 1/1 listened
    res_it = client.get("/api/progress", headers={"Authorization": f"Bearer {token}"})
    assert res_it.status_code == 200
    assert res_it.json()["listenedWords"] == 1
    assert res_it.json()["language"] == "it"

    # Switch to Danish
    client.patch("/api/profile", json={"hostId": "anders"}, headers={"Authorization": f"Bearer {token}"})

    # Danish progress: 0/1 listened
    res_da = client.get("/api/progress", headers={"Authorization": f"Bearer {token}"})
    assert res_da.json()["listenedWords"] == 0
    assert res_da.json()["language"] == "da"

    # Switch back to Italian — progress still there
    client.patch("/api/profile", json={"hostId": "marco"}, headers={"Authorization": f"Bearer {token}"})

    res_back = client.get("/api/progress", headers={"Authorization": f"Bearer {token}"})
    assert res_back.json()["listenedWords"] == 1


# ---------- Progress includes per-category breakdown ----------


def test_progress_per_category_breakdown(client: TestClient) -> None:
    token = _register(client, "e2e_catprog@example.com", host_id="marco")
    _seed_multilang()

    res = client.get("/api/progress", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert data["totalWords"] >= 1
    assert len(data["categories"]) >= 1
    cat = data["categories"][0]
    assert "id" in cat
    assert "totalWords" in cat
    assert "listenedWords" in cat


# ---------- User word contribution full lifecycle ----------


@patch("app.routers.dictionary.get_audio_path", return_value=None)
def test_contribute_word_lifecycle(mock_audio, client: TestClient) -> None:
    """Register → contribute word → find in search → see in categories."""
    token = _register(client, "e2e_ugc@example.com", host_id="marco")

    # Seed a category for assignment
    db = SessionLocal()
    db.add(Category(id="cat-ugc-e2e", name_en="Custom", name_da="Tilpasset", name_it="Personalizzato", order=5))
    db.commit()
    db.close()

    # Contribute a word
    res = client.post(
        "/api/dictionary/words",
        json={
            "word": "arrivederci",
            "translation": "goodbye",
            "phoneticHint": "ah-ree-veh-DEHR-chee",
            "categoryId": "cat-ugc-e2e",
            "difficulty": "intermediate",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    word_data = res.json()
    assert word_data["source"] == "user"
    word_id = word_data["id"]

    # Verify it appears in search
    search_res = client.get("/api/search?q=arrivederci", headers={"Authorization": f"Bearer {token}"})
    assert len(search_res.json()["results"]) >= 1

    # Verify it appears in category words
    cat_res = client.get(
        "/api/dictionary/categories/cat-ugc-e2e/words",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert any(w["word"] == "arrivederci" for w in cat_res.json()["words"])

    # Mark listened and verify progress
    client.post(f"/api/dictionary/words/{word_id}/listened", headers={"Authorization": f"Bearer {token}"})
    progress_res = client.get("/api/progress", headers={"Authorization": f"Bearer {token}"})
    assert progress_res.json()["listenedWords"] >= 1


# ---------- Duplicate detection ----------


@patch("app.routers.dictionary.get_audio_path", return_value=None)
def test_contribute_duplicate_word_409(mock_audio, client: TestClient) -> None:
    token = _register(client, "e2e_dup@example.com", host_id="marco")

    client.post(
        "/api/dictionary/words",
        json={"word": "sole", "translation": "sun"},
        headers={"Authorization": f"Bearer {token}"},
    )
    res = client.post(
        "/api/dictionary/words",
        json={"word": "sole", "translation": "sun again"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 409
    assert "existingWordId" in res.json()


# ---------- GDPR: Delete user cascades progress ----------


def test_gdpr_delete_removes_progress(client: TestClient) -> None:
    """Deleting a user removes their progress records."""
    token = _register(client, "e2e_gdpr@example.com", host_id="marco")
    _seed_multilang()

    # Create progress
    client.post("/api/dictionary/words/w-ciao/listened", headers={"Authorization": f"Bearer {token}"})

    # Verify progress exists
    db = SessionLocal()
    count_before = db.query(UserProgress).count()
    db.close()
    assert count_before >= 1

    # Delete account
    res = client.delete("/api/profile", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200

    # Verify progress gone
    db = SessionLocal()
    count_after = db.query(UserProgress).count()
    db.close()
    assert count_after == 0


# ---------- Reference language parameter ----------


def test_reference_language_switches_translations(client: TestClient) -> None:
    """?lang= parameter changes translation and category names."""
    token = _register(client, "e2e_ref@example.com", host_id="marco")
    _seed_multilang()

    # Default ref lang for Italian target is "en"
    res_en = client.get("/api/dictionary/categories?lang=en", headers={"Authorization": f"Bearer {token}"})
    cat_en = next(c for c in res_en.json()["categories"] if c["id"] == "cat-greet")
    assert cat_en["name"] == "Greetings"

    # Switch ref to Danish
    res_da = client.get("/api/dictionary/categories?lang=da", headers={"Authorization": f"Bearer {token}"})
    cat_da = next(c for c in res_da.json()["categories"] if c["id"] == "cat-greet")
    assert cat_da["name"] == "Hilsner"


# ---------- Audio language mismatch ----------


def test_audio_rejects_wrong_language_word(client: TestClient) -> None:
    """Italian host can't get audio for Danish word."""
    token = _register(client, "e2e_audio@example.com", host_id="marco")
    _seed_multilang()

    res = client.get("/api/audio/w-hej", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 400


# ---------- Progress endpoint requires auth ----------


def test_progress_requires_auth(client: TestClient) -> None:
    res = client.get("/api/progress")
    assert res.status_code == 401


# ---------- Full E2E flow ----------


@patch("app.routers.dictionary.get_audio_path", return_value=None)
def test_full_e2e_flow(mock_audio, client: TestClient) -> None:
    """Register → select host → browse words → contribute word → switch host → verify isolation."""
    _seed_multilang()

    # 1. Register
    reg = client.post(
        "/api/auth/register",
        json={"email": "e2e_full@example.com", "password": "Password1"},
    )
    assert reg.status_code == 200
    token = reg.json()["token"]

    # 2. Select Italian host
    client.patch("/api/profile", json={"hostId": "giulia"}, headers={"Authorization": f"Bearer {token}"})

    # 3. Browse Italian words
    cats = client.get("/api/dictionary/categories", headers={"Authorization": f"Bearer {token}"})
    assert cats.status_code == 200

    words = client.get("/api/dictionary/categories/cat-greet/words", headers={"Authorization": f"Bearer {token}"})
    assert words.json()["words"][0]["word"] == "ciao"

    # 4. Listen to word
    client.post("/api/dictionary/words/w-ciao/listened", headers={"Authorization": f"Bearer {token}"})

    # 5. Contribute a new word
    contrib = client.post(
        "/api/dictionary/words",
        json={"word": "buongiorno", "translation": "good morning"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert contrib.status_code == 200

    # 6. Verify progress
    progress = client.get("/api/progress", headers={"Authorization": f"Bearer {token}"})
    assert progress.json()["listenedWords"] >= 1
    assert progress.json()["language"] == "it"

    # 7. Switch to Danish host
    client.patch("/api/profile", json={"hostId": "freja"}, headers={"Authorization": f"Bearer {token}"})

    # 8. Verify progress isolation
    da_progress = client.get("/api/progress", headers={"Authorization": f"Bearer {token}"})
    assert da_progress.json()["listenedWords"] == 0
    assert da_progress.json()["language"] == "da"

    # 9. Switch back to Italian — progress preserved
    client.patch("/api/profile", json={"hostId": "giulia"}, headers={"Authorization": f"Bearer {token}"})
    it_progress = client.get("/api/progress", headers={"Authorization": f"Bearer {token}"})
    assert it_progress.json()["listenedWords"] >= 1


# ---------- Progress category names respect user's reference language (Task 039) ----------


def _register_with_lang(client: TestClient, email: str, host_id: str, language: str) -> str:
    """Register a user with a specific reference language and host."""
    res = client.post(
        "/api/auth/register",
        json={"email": email, "password": "Password1", "language": language},
    )
    assert res.status_code == 200
    token = res.json()["token"]
    client.patch("/api/profile", json={"hostId": host_id}, headers={"Authorization": f"Bearer {token}"})
    return token


def test_progress_category_names_italian_ref_lang(client: TestClient) -> None:
    """Italian-speaking user learning Danish sees Italian category names in progress."""
    _seed_multilang()
    token = _register_with_lang(client, "prog_it@example.com", host_id="anders", language="it")

    res = client.get("/api/progress", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert data["language"] == "da"
    cat = next(c for c in data["categories"] if c["id"] == "cat-greet")
    assert cat["name"] == "Saluti"


def test_progress_category_names_danish_ref_lang(client: TestClient) -> None:
    """Danish-speaking user learning Italian sees Danish category names in progress."""
    _seed_multilang()
    token = _register_with_lang(client, "prog_da@example.com", host_id="marco", language="da")

    res = client.get("/api/progress", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert data["language"] == "it"
    cat = next(c for c in data["categories"] if c["id"] == "cat-greet")
    assert cat["name"] == "Hilsner"


def test_progress_category_names_english_ref_lang(client: TestClient) -> None:
    """English-speaking user learning Italian sees English category names in progress."""
    _seed_multilang()
    token = _register_with_lang(client, "prog_en@example.com", host_id="marco", language="en")

    res = client.get("/api/progress", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert data["language"] == "it"
    cat = next(c for c in data["categories"] if c["id"] == "cat-greet")
    assert cat["name"] == "Greetings"


def test_progress_counts_unaffected_by_ref_lang_fix(client: TestClient) -> None:
    """Verify progress totals and listened counts are unaffected by the ref_lang fix."""
    _seed_multilang()
    token = _register_with_lang(client, "prog_count@example.com", host_id="marco", language="da")

    # Listen to the Italian word
    client.post("/api/dictionary/words/w-ciao/listened", headers={"Authorization": f"Bearer {token}"})

    res = client.get("/api/progress", headers={"Authorization": f"Bearer {token}"})
    data = res.json()
    assert data["totalWords"] >= 1
    assert data["listenedWords"] == 1
    cat = next(c for c in data["categories"] if c["id"] == "cat-greet")
    assert cat["listenedWords"] == 1
    assert cat["totalWords"] == 1
