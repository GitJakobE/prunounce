from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_ok() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["database_writable"] is True
    assert data["audio_cache_writable"] is True


@patch("app.routers.health._check_db_writable", return_value=False)
def test_health_degraded_when_db_not_writable(mock_db) -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "degraded"
    assert data["database_writable"] is False
    assert data["audio_cache_writable"] is True


@patch("app.routers.health._check_audio_cache_writable", return_value=False)
def test_health_degraded_when_audio_cache_not_writable(mock_audio) -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "degraded"
    assert data["database_writable"] is True
    assert data["audio_cache_writable"] is False


@patch("app.routers.health._check_db_writable", return_value=False)
@patch("app.routers.health._check_audio_cache_writable", return_value=False)
def test_health_degraded_when_both_not_writable(mock_audio, mock_db) -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "degraded"
    assert data["database_writable"] is False
    assert data["audio_cache_writable"] is False
