from fastapi.testclient import TestClient

from app.rate_limit import _store


def register(client: TestClient, email: str = "auth@example.com", password: str = "Password1", language: str = "en") -> dict:
    return client.post(
        "/api/auth/register",
        json={"email": email, "password": password, "language": language},
    ).json()


def register_and_token(client: TestClient, email: str = "auth@example.com") -> str:
    res = client.post(
        "/api/auth/register",
        json={"email": email, "password": "Password1", "language": "en"},
    )
    assert res.status_code == 200
    return res.json()["token"]


# ---------- Registration ----------


def test_register_success(client: TestClient) -> None:
    res = client.post(
        "/api/auth/register",
        json={"email": "new@example.com", "password": "Password1", "language": "en"},
    )
    assert res.status_code == 200
    data = res.json()
    assert "token" in data
    assert data["user"]["email"] == "new@example.com"
    assert data["user"]["language"] == "en"
    assert "id" in data["user"]


def test_register_defaults_language_to_en(client: TestClient) -> None:
    res = client.post(
        "/api/auth/register",
        json={"email": "default@example.com", "password": "Password1"},
    )
    assert res.status_code == 200
    assert res.json()["user"]["language"] == "en"


def test_register_duplicate_email(client: TestClient) -> None:
    client.post(
        "/api/auth/register",
        json={"email": "dup@example.com", "password": "Password1", "language": "en"},
    )
    res = client.post(
        "/api/auth/register",
        json={"email": "dup@example.com", "password": "Password1", "language": "en"},
    )
    assert res.status_code == 409


def test_register_case_insensitive_email(client: TestClient) -> None:
    client.post(
        "/api/auth/register",
        json={"email": "UPPER@example.com", "password": "Password1", "language": "en"},
    )
    res = client.post(
        "/api/auth/register",
        json={"email": "upper@example.com", "password": "Password1", "language": "en"},
    )
    assert res.status_code == 409


def test_register_weak_password_no_uppercase(client: TestClient) -> None:
    res = client.post(
        "/api/auth/register",
        json={"email": "weak@example.com", "password": "password1"},
    )
    assert res.status_code == 400


def test_register_weak_password_no_digit(client: TestClient) -> None:
    res = client.post(
        "/api/auth/register",
        json={"email": "weak2@example.com", "password": "Password"},
    )
    assert res.status_code == 400


def test_register_weak_password_too_short(client: TestClient) -> None:
    res = client.post(
        "/api/auth/register",
        json={"email": "weak3@example.com", "password": "Pa1"},
    )
    assert res.status_code == 400


def test_register_invalid_language(client: TestClient) -> None:
    res = client.post(
        "/api/auth/register",
        json={"email": "lang@example.com", "password": "Password1", "language": "xx"},
    )
    assert res.status_code == 400


def test_register_stores_display_name(client: TestClient) -> None:
    res = client.post(
        "/api/auth/register",
        json={
            "email": "withname@example.com",
            "password": "Password1",
            "displayName": "Test User",
        },
    )
    assert res.status_code == 200
    assert res.json()["user"]["displayName"] == "Test User"


# ---------- Login ----------


def test_login_success(client: TestClient) -> None:
    _store.clear()
    client.post(
        "/api/auth/register",
        json={"email": "login@example.com", "password": "Password1", "language": "en"},
    )
    res = client.post(
        "/api/auth/login",
        json={"email": "login@example.com", "password": "Password1"},
    )
    assert res.status_code == 200
    data = res.json()
    assert "token" in data
    assert data["user"]["email"] == "login@example.com"


def test_login_case_insensitive(client: TestClient) -> None:
    _store.clear()
    client.post(
        "/api/auth/register",
        json={"email": "caselogin@example.com", "password": "Password1", "language": "en"},
    )
    res = client.post(
        "/api/auth/login",
        json={"email": "CaseLogin@example.com", "password": "Password1"},
    )
    assert res.status_code == 200
    assert res.json()["user"]["email"] == "caselogin@example.com"


def test_login_wrong_password(client: TestClient) -> None:
    _store.clear()
    client.post(
        "/api/auth/register",
        json={"email": "wp@example.com", "password": "Password1", "language": "en"},
    )
    res = client.post(
        "/api/auth/login",
        json={"email": "wp@example.com", "password": "WrongPass1"},
    )
    assert res.status_code == 401


def test_login_nonexistent_email(client: TestClient) -> None:
    _store.clear()
    res = client.post(
        "/api/auth/login",
        json={"email": "nobody@example.com", "password": "Password1"},
    )
    assert res.status_code == 401


# ---------- GET /me ----------


def test_me_returns_current_user(client: TestClient) -> None:
    token = register_and_token(client, "me@example.com")
    res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["user"]["email"] == "me@example.com"


def test_me_requires_auth(client: TestClient) -> None:
    res = client.get("/api/auth/me")
    assert res.status_code == 401


def test_me_rejects_invalid_token(client: TestClient) -> None:
    res = client.get("/api/auth/me", headers={"Authorization": "Bearer bad.token.here"})
    assert res.status_code == 401


# ---------- Google OAuth stub ----------


def test_google_returns_501(client: TestClient) -> None:
    res = client.post("/api/auth/google")
    assert res.status_code == 501
