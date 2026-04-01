import time
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.rate_limit import MAX_ATTEMPTS, WINDOW_SECONDS, _store


def _register(client: TestClient, email: str = "ratelimit@example.com") -> None:
    client.post(
        "/api/auth/register",
        json={"email": email, "password": "Password1", "language": "en"},
    )


def test_rate_limit_blocks_after_max_failures(client: TestClient) -> None:
    _store.clear()
    email = "block@example.com"
    _register(client, email)

    for _ in range(MAX_ATTEMPTS):
        client.post("/api/auth/login", json={"email": email, "password": "Wrong1234"})

    res = client.post("/api/auth/login", json={"email": email, "password": "Wrong1234"})
    assert res.status_code == 429


def test_rate_limit_allows_before_max(client: TestClient) -> None:
    _store.clear()
    email = "partialblock@example.com"
    _register(client, email)

    for _ in range(MAX_ATTEMPTS - 1):
        res = client.post("/api/auth/login", json={"email": email, "password": "Wrong1234"})
        assert res.status_code == 401

    # Next attempt still goes through (returns 401, not 429)
    res = client.post("/api/auth/login", json={"email": email, "password": "Wrong1234"})
    assert res.status_code == 401


def test_rate_limit_resets_on_success(client: TestClient) -> None:
    _store.clear()
    email = "resetok@example.com"
    _register(client, email)

    for _ in range(MAX_ATTEMPTS - 1):
        client.post("/api/auth/login", json={"email": email, "password": "Wrong1234"})

    # Login with correct password resets counter
    res = client.post("/api/auth/login", json={"email": email, "password": "Password1"})
    assert res.status_code == 200

    # More failed attempts should be allowed again
    for _ in range(MAX_ATTEMPTS - 1):
        res = client.post("/api/auth/login", json={"email": email, "password": "Wrong1234"})
        assert res.status_code == 401


def test_rate_limit_case_insensitive(client: TestClient) -> None:
    _store.clear()
    email = "case@example.com"
    _register(client, email)

    for _ in range(MAX_ATTEMPTS):
        # Alternate casing
        client.post("/api/auth/login", json={"email": "CASE@example.com", "password": "Wrong1234"})

    res = client.post("/api/auth/login", json={"email": "case@example.com", "password": "Wrong1234"})
    assert res.status_code == 429


def test_rate_limit_window_expires(client: TestClient) -> None:
    _store.clear()
    email = "expire@example.com"
    _register(client, email)

    # Simulate attempts that happened long ago
    past = time.time() - WINDOW_SECONDS - 10
    _store[email.lower()] = (MAX_ATTEMPTS, past)

    res = client.post("/api/auth/login", json={"email": email, "password": "Wrong1234"})
    # Should not be 429 because window expired
    assert res.status_code == 401
