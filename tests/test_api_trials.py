from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_trials_pagination_shape():
    r = client.get("/trials?limit=5&page=1")
    assert r.status_code == 200
    data = r.json()
    assert set(data.keys()) == {"page", "limit", "total", "pages", "items"}
    assert data["page"] == 1
    assert data["limit"] == 5
    assert isinstance(data["items"], list)


def test_trials_filter_does_not_error():
    r = client.get("/trials?q=cancer&limit=5")
    assert r.status_code == 200

