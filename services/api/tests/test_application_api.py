from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_telemetry_updates_charger_status():
    response = client.post(
        "/api/v1/telemetry",
        json={
            "charger_id": "charger-test-api-1",
            "connector_id": "connector-1",
            "power_kw": 11.0,
            "voltage": 230.0,
            "current_amp": 16.0,
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "occupied"


def test_start_and_end_charging_session():
    start_response = client.post(
        "/api/v1/sessions/start",
        json={
            "charger_id": "charger-test-api-2",
            "connector_id": "connector-1",
            "user_id": "user-1",
        },
    )

    assert start_response.status_code == 200
    session_id = start_response.json()["session_id"]

    end_response = client.post(
        f"/api/v1/sessions/{session_id}/end",
        json={"energy_delivered_kwh": 22.5},
    )

    assert end_response.status_code == 200
    assert end_response.json()["status"] == "ended"
    assert end_response.json()["energy_delivered_kwh"] == 22.5