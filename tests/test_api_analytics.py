from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_top_conditions_shape():
    r = client.get("/analytics/top-conditions?limit=5")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    if data:
        assert set(data[0].keys()) == {"name", "count"}


def test_trials_over_time_month_shape():
    r = client.get("/analytics/trials-over-time?interval=month")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    if data:
        assert set(data[0].keys()) == {"period", "count"}


def test_sponsor_breakdown_shape():
    r = client.get("/analytics/sponsor-breakdown?limit=5")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    if data:
        assert set(data[0].keys()) == {"name", "count"}

