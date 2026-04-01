from fastapi.testclient import TestClient

from app.models import Category, Word, WordCategory, UserProgress

from .conftest import TestSessionLocal as SessionLocal


def register_and_token(client: TestClient, email: str = "profile@example.com", host_id: str | None = None) -> str:
    res = client.post(
        "/api/auth/register",
        json={"email": email, "password": "Password1", "language": "en"},
    )
    assert res.status_code == 200
    token = res.json()["token"]

    if host_id:
        client.patch(
            "/api/profile",
            json={"hostId": host_id},
            headers={"Authorization": f"Bearer {token}"},
        )
    return token


# ---------- GET /api/profile ----------


def test_get_profile_returns_user_and_progress(client: TestClient) -> None:
    token = register_and_token(client)

    res = client.get("/api/profile", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert data["user"]["email"] == "profile@example.com"
    assert "createdAt" in data["user"]
    assert data["progress"]["totalWords"] >= 0
    assert data["progress"]["listenedWords"] >= 0


def test_get_profile_progress_counts_correct_language(client: TestClient) -> None:
    token = register_and_token(client, "progress@example.com", host_id="marco")

    # Seed Italian word and mark it listened
    db = SessionLocal()
    word = Word(
        id="w-profile-test",
        word="test",
        language="it",
        phonetic_hint="test",
        translation_en="test",
        translation_da="test",
        translation_it="test",
        difficulty="beginner",
        source="seed",
    )
    db.add(word)
    db.commit()

    # Mark listened via API
    res_listen = client.post(
        "/api/dictionary/words/w-profile-test/listened",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res_listen.status_code == 200
    db.close()

    res = client.get("/api/profile", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["progress"]["listenedWords"] >= 1


def test_get_profile_requires_auth(client: TestClient) -> None:
    res = client.get("/api/profile")
    assert res.status_code == 401


# ---------- PATCH /api/profile ----------


def test_update_display_name(client: TestClient) -> None:
    token = register_and_token(client, "patchname@example.com")

    res = client.patch(
        "/api/profile",
        json={"displayName": "New Name"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    assert res.json()["user"]["displayName"] == "New Name"


def test_update_language(client: TestClient) -> None:
    token = register_and_token(client, "patchlang@example.com")

    res = client.patch(
        "/api/profile",
        json={"language": "da"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    assert res.json()["user"]["language"] == "da"


def test_update_host_id(client: TestClient) -> None:
    token = register_and_token(client, "patchhost@example.com")

    res = client.patch(
        "/api/profile",
        json={"hostId": "giulia"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    assert res.json()["user"]["hostId"] == "giulia"


def test_update_invalid_language_rejected(client: TestClient) -> None:
    token = register_and_token(client, "badlang@example.com")

    res = client.patch(
        "/api/profile",
        json={"language": "zz"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 400


def test_update_invalid_host_rejected(client: TestClient) -> None:
    token = register_and_token(client, "badhost@example.com")

    res = client.patch(
        "/api/profile",
        json={"hostId": "nosuchhost"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 400


def test_update_empty_body_rejected(client: TestClient) -> None:
    token = register_and_token(client, "noop@example.com")

    res = client.patch(
        "/api/profile",
        json={},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 400


# ---------- DELETE /api/profile ----------


def test_delete_profile_removes_user(client: TestClient) -> None:
    token = register_and_token(client, "deleteme@example.com")

    res = client.delete("/api/profile", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert "deleted" in res.json()["message"].lower()

    # Verify user is gone
    me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 404


def test_delete_cascades_progress(client: TestClient) -> None:
    token = register_and_token(client, "cascadedel@example.com", host_id="marco")

    # Seed a word and mark listened
    db = SessionLocal()
    word = Word(
        id="w-cascade-del",
        word="ciao",
        language="it",
        phonetic_hint="chow",
        translation_en="hello",
        translation_da="hej",
        translation_it="ciao",
        difficulty="beginner",
        source="seed",
    )
    db.add(word)
    db.commit()
    db.close()

    client.post(
        "/api/dictionary/words/w-cascade-del/listened",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Delete
    res = client.delete("/api/profile", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200

    # Progress should be gone
    db = SessionLocal()
    count = db.query(UserProgress).count()
    db.close()
    assert count == 0
