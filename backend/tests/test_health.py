"""Tests for the public liveness endpoint."""

from fastapi.testclient import TestClient

from healthscope.config import Settings
from healthscope.main import create_app


def test_health_check_returns_service_metadata() -> None:
    settings = Settings(app_name="HealthScope Test", environment="test")

    with TestClient(create_app(settings)) as client:
        response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "HealthScope Test",
        "version": "0.1.0",
        "environment": "test",
    }


def test_openapi_schema_exposes_health_endpoint() -> None:
    with TestClient(create_app(Settings(environment="test"))) as client:
        response = client.get("/openapi.json")

    assert response.status_code == 200
    assert "/api/v1/health" in response.json()["paths"]
