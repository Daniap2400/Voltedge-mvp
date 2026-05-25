from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_unknown_charger_returns_404():
    response = client.get("/api/v1/chargers/unknown-charger/status")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_end_unknown_session_returns_404():
    response = client.post(
        "/api/v1/sessions/unknown-session/end",
        json={"energy_delivered_kwh": 10.5},
    )

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_telemetry_with_negative_power_returns_422():
    response = client.post(
        "/api/v1/telemetry",
        json={
            "charger_id": "charger-1",
            "connector_id": "connector-1",
            "power_kw": -1,
            "voltage": 230,
            "current_amp": 16,
        },
    )

    assert response.status_code == 422


def test_telemetry_with_empty_charger_id_returns_422():
    response = client.post(
        "/api/v1/telemetry",
        json={
            "charger_id": "",
            "connector_id": "connector-1",
            "power_kw": 11,
            "voltage": 230,
            "current_amp": 16,
        },
    )

    assert response.status_code == 422


def test_start_session_with_empty_connector_id_returns_422():
    response = client.post(
        "/api/v1/sessions/start",
        json={
            "charger_id": "charger-1",
            "connector_id": "",
            "user_id": "user-1",
            "contract_id": "contract-1",
        },
    )

    assert response.status_code == 422