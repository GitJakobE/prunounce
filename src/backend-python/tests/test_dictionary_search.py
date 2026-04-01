from fastapi.testclient import TestClient

from app.models import Category, Word, WordCategory

from .conftest import TestSessionLocal as SessionLocal


def register_and_token(client: TestClient, email: str = "dict@example.com", host_id: str = "marco") -> str:
    res = client.post(
        "/api/auth/register",
        json={"email": email, "password": "Password1", "language": "en"},
    )
    assert res.status_code == 200
    token = res.json()["token"]
    # Set host for target language
    client.patch(
        "/api/profile",
        json={"hostId": host_id},
        headers={"Authorization": f"Bearer {token}"},
    )
    return token


def seed_data(language: str = "it") -> tuple[str, str]:
    cat_id = "cat-food"
    word_id = "w-bruschetta"
    db = SessionLocal()
    cat = Category(id=cat_id, name_en="Food", name_da="Mad", name_it="Cibo", order=1)
    w = Word(
        id=word_id,
        word="bruschetta",
        language=language,
        phonetic_hint="broo-SKET-tah",
        translation_en="bruschetta",
        translation_da="bruschetta",
        translation_it="bruschetta",
        difficulty="beginner",
        example_it="Mi piace la bruschetta.",
        example_en="I like bruschetta.",
        example_da="Jeg kan lide bruschetta.",
        source="seed",
    )
    db.add(cat)
    db.add(w)
    db.flush()
    db.add(WordCategory(word_id=word_id, category_id=cat_id))
    db.commit()
    db.close()
    return cat_id, word_id


def seed_multi_difficulty() -> str:
    db = SessionLocal()
    cat = Category(id="cat-multi", name_en="Multi", name_da="Multi", name_it="Multi", order=2)
    db.add(cat)
    for diff in ("beginner", "intermediate", "advanced"):
        w = Word(
            id=f"w-{diff}",
            word=f"word_{diff}",
            language="it",
            phonetic_hint="hint",
            translation_en="translation",
            translation_da="oversættelse",
            translation_it="traduzione",
            difficulty=diff,
            source="seed",
        )
        db.add(w)
        db.flush()
        db.add(WordCategory(word_id=w.id, category_id=cat.id))
    db.commit()
    db.close()
    return "cat-multi"


# ---------- Categories ----------


def test_categories_returns_list(client: TestClient) -> None:
    token = register_and_token(client)
    seed_data()

    res = client.get("/api/dictionary/categories", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    cats = res.json()["categories"]
    assert len(cats) >= 1
    assert cats[0]["id"] == "cat-food"
    assert cats[0]["totalWords"] == 1


def test_categories_includes_progress_by_difficulty(client: TestClient) -> None:
    token = register_and_token(client, "catprog@example.com")
    seed_multi_difficulty()

    res = client.get("/api/dictionary/categories", headers={"Authorization": f"Bearer {token}"})
    cat = next(c for c in res.json()["categories"] if c["id"] == "cat-multi")
    assert len(cat["progressByDifficulty"]) == 3
    difficulties = {p["difficulty"] for p in cat["progressByDifficulty"]}
    assert difficulties == {"beginner", "intermediate", "advanced"}


def test_categories_requires_auth(client: TestClient) -> None:
    res = client.get("/api/dictionary/categories")
    assert res.status_code == 401


# ---------- Category Words ----------


def test_category_words_returns_words(client: TestClient) -> None:
    token = register_and_token(client)
    category_id, _ = seed_data()

    res = client.get(
        f"/api/dictionary/categories/{category_id}/words",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["category"]["id"] == category_id
    assert len(data["words"]) == 1
    word = data["words"][0]
    assert word["word"] == "bruschetta"
    assert "phoneticHint" in word
    assert "translation" in word
    assert word["listened"] is False


def test_category_words_filter_by_difficulty(client: TestClient) -> None:
    token = register_and_token(client, "difffilter@example.com")
    category_id = seed_multi_difficulty()

    res = client.get(
        f"/api/dictionary/categories/{category_id}/words?difficulty=beginner",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    words = res.json()["words"]
    assert all(w["difficulty"] == "beginner" for w in words)
    assert len(words) == 1


def test_category_not_found(client: TestClient) -> None:
    token = register_and_token(client, "catnotfound@example.com")

    res = client.get(
        "/api/dictionary/categories/nonexistent/words",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 404


# ---------- Mark Listened ----------


def test_mark_listened_creates_progress(client: TestClient) -> None:
    token = register_and_token(client)
    category_id, word_id = seed_data()

    res = client.post(
        f"/api/dictionary/words/{word_id}/listened",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    assert res.json() == {"listened": True}

    # Confirm the word is now marked listened
    words_res = client.get(
        f"/api/dictionary/categories/{category_id}/words",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert words_res.json()["words"][0]["listened"] is True


def test_mark_listened_idempotent(client: TestClient) -> None:
    token = register_and_token(client, "idem@example.com")
    _, word_id = seed_data()

    # Mark twice
    client.post(f"/api/dictionary/words/{word_id}/listened", headers={"Authorization": f"Bearer {token}"})
    res = client.post(f"/api/dictionary/words/{word_id}/listened", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200


def test_mark_listened_word_not_found(client: TestClient) -> None:
    token = register_and_token(client, "listennotfound@example.com")

    res = client.post(
        "/api/dictionary/words/nonexistent/listened",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 404


# ---------- Search ----------


def test_search_returns_ranked_results(client: TestClient) -> None:
    token = register_and_token(client, "search1@example.com")
    seed_data()

    res = client.get("/api/search?q=bruschetta", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    results = res.json()["results"]
    assert len(results) >= 1
    assert results[0]["word"] == "bruschetta"


def test_search_prefix_match(client: TestClient) -> None:
    token = register_and_token(client, "search2@example.com")
    seed_data()

    res = client.get("/api/search?q=brus", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert len(res.json()["results"]) == 1


def test_search_too_short(client: TestClient) -> None:
    token = register_and_token(client, "searchshort@example.com")

    res = client.get("/api/search?q=a", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 400


def test_search_no_results(client: TestClient) -> None:
    token = register_and_token(client, "searchnone@example.com")
    seed_data()

    res = client.get("/api/search?q=zzzzz", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["results"] == []
    assert "message" in res.json()


def test_search_diacritic_normalization(client: TestClient) -> None:
    """Search with diacritics should still match normalized words."""
    token = register_and_token(client, "searchdia@example.com")

    db = SessionLocal()
    db.add(Word(
        id="w-caffe",
        word="caffè",
        language="it",
        phonetic_hint="kaf-FEH",
        translation_en="coffee",
        translation_da="kaffe",
        translation_it="caffè",
        difficulty="beginner",
        source="seed",
    ))
    db.commit()
    db.close()

    # Search without accent
    res = client.get("/api/search?q=caffe", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert len(res.json()["results"]) >= 1


def test_search_by_translation(client: TestClient) -> None:
    token = register_and_token(client, "searchtr@example.com")
    seed_data()

    # Search by English translation
    res = client.get("/api/search?q=bruschetta", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert len(res.json()["results"]) >= 1


def test_search_requires_auth(client: TestClient) -> None:
    res = client.get("/api/search?q=hello")
    assert res.status_code == 401


# ---------- Multi-language dictionary ----------


def test_danish_host_sees_danish_words(client: TestClient) -> None:
    """User with Danish host should see Danish words."""
    token = register_and_token(client, "dadict@example.com", host_id="anders")

    db = SessionLocal()
    cat = Category(id="cat-da", name_en="Greetings", name_da="Hilsner", name_it="Saluti", order=3)
    w = Word(
        id="w-hej",
        word="hej",
        language="da",
        phonetic_hint="hai",
        translation_en="hello",
        translation_da="hej",
        translation_it="ciao",
        difficulty="beginner",
        source="seed",
    )
    db.add(cat)
    db.add(w)
    db.flush()
    db.add(WordCategory(word_id=w.id, category_id=cat.id))
    db.commit()
    db.close()

    res = client.get(
        "/api/dictionary/categories/cat-da/words",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    words = res.json()["words"]
    assert len(words) == 1
    assert words[0]["word"] == "hej"
