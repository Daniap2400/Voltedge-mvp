from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_analytics_summary_endpoint_returns_expected_fields():
    response = client.get("/api/v1/analytics/summary")

    assert response.status_code == 200

    data = response.json()

    assert "charger_count" in data
    assert "session_count" in data
    assert "ended_session_count" in data
    assert "total_energy_delivered_kwh" in data
    assert "average_session_duration_minutes" in data
    assert "utilization_rate" in data
    assert "charger_fault_rate" in data
    assert "expected_demand_kwh" in data
    assert "anomalies" in data


def test_charger_analytics_endpoint_returns_404_for_unknown_charger():
    response = client.get("/api/v1/analytics/chargers/unknown-charger")

    assert response.status_code == 404