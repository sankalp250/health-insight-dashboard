"""API integration tests for the Health Insight Dashboard backend."""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_list_vaccines_returns_data():
    """`/api/vaccines` should return records and pagination metadata."""
    response = client.get("/api/vaccines")
    assert response.status_code == 200

    payload = response.json()
    assert payload["total"] > 0
    assert payload["returned"] == len(payload["data"])
    first_record = payload["data"][0]
    assert {"region", "brand", "year"}.issubset(first_record.keys())


def test_list_vaccines_filters_by_region_and_brand():
    """Query parameters should narrow the dataset."""
    response = client.get("/api/vaccines", params={"region": "Asia", "brand": "Pfizer"})
    assert response.status_code == 200

    payload = response.json()
    assert payload["total"] > 0
    for record in payload["data"]:
        assert record["region"] == "Asia"
        assert record["brand"] == "Pfizer"


def test_summary_endpoint_returns_kpis():
    """`/api/summary` should return KPI metrics with descriptions."""
    response = client.get("/api/summary")
    assert response.status_code == 200

    payload = response.json()
    assert len(payload["kpis"]) >= 3
    for kpi in payload["kpis"]:
        assert "label" in kpi and kpi["label"]
        assert "value" in kpi
        assert "description" in kpi


