from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint_returns_running_service():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["service"] == "voltedge-api"
    assert response.json()["status"] == "running"


def test_root_health_endpoint_returns_healthy_status():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_v1_health_endpoint_returns_healthy_status():
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["api_version"] == "v1"