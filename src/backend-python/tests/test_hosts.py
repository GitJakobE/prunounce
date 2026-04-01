from fastapi.testclient import TestClient


def test_list_hosts_returns_all(client: TestClient) -> None:
    res = client.get("/api/hosts")
    assert res.status_code == 200
    hosts = res.json()["hosts"]
    assert len(hosts) == 12


def test_hosts_no_auth_required(client: TestClient) -> None:
    # No Authorization header
    res = client.get("/api/hosts")
    assert res.status_code == 200


def test_hosts_have_required_fields(client: TestClient) -> None:
    res = client.get("/api/hosts")
    hosts = res.json()["hosts"]
    required = {"id", "name", "language", "emoji", "imageUrl", "color", "voice"}
    for host in hosts:
        assert required.issubset(host.keys()), f"Host {host.get('id')} missing fields"
        assert host["voice"]["voiceName"]


def test_hosts_cover_all_languages(client: TestClient) -> None:
    res = client.get("/api/hosts")
    hosts = res.json()["hosts"]
    languages = {h["language"] for h in hosts}
    assert languages == {"it", "da", "en"}


def test_hosts_four_per_language(client: TestClient) -> None:
    res = client.get("/api/hosts")
    hosts = res.json()["hosts"]
    for lang in ("it", "da", "en"):
        count = sum(1 for h in hosts if h["language"] == lang)
        assert count == 4, f"Expected 4 hosts for {lang}, got {count}"
