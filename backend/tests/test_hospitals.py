"""Tests for the public hospital endpoint."""

from datetime import UTC, datetime

from fastapi.testclient import TestClient

from healthscope.clients.cms import (
    CMSClient,
    CMSDataError,
    CMSUpstreamTimeoutError,
    get_cms_client,
)
from healthscope.config import Settings
from healthscope.main import create_app
from healthscope.schemas.hospitals import Hospital, HospitalDataSource, HospitalPage


def hospital_page() -> HospitalPage:
    """Return an API page based on an official CMS hospital record."""

    return HospitalPage(
        items=[
            Hospital(
                facility_id="010001",
                facility_name="SOUTHEAST HEALTH MEDICAL CENTER",
                address="1108 ROSS CLARK CIRCLE",
                city="DOTHAN",
                state="AL",
                zip_code="36301",
                county="HOUSTON",
                telephone="(334) 793-8701",
                hospital_type="Acute Care Hospitals",
                ownership="Government - Hospital District or Authority",
                emergency_services=True,
                birthing_friendly=True,
                overall_rating=4,
            )
        ],
        total=5432,
        limit=1,
        offset=5,
        source=HospitalDataSource(
            name="Centers for Medicare & Medicaid Services",
            dataset_name="Hospital General Information",
            dataset_url="https://data.cms.gov/provider-data/dataset/xubh-q36u",
            retrieved_at=datetime(2026, 7, 18, tzinfo=UTC),
        ),
    )


class StubCMSClient:
    """Controllable CMS client used by endpoint tests."""

    def __init__(self, result: HospitalPage | Exception) -> None:
        self.result = result

    async def fetch_hospitals(self, *, limit: int, offset: int) -> HospitalPage:
        assert limit == 1
        assert offset == 5
        if isinstance(self.result, Exception):
            raise self.result
        return self.result


def client_for(result: HospitalPage | Exception) -> TestClient:
    """Create an app with its CMS boundary replaced by a stub."""

    app = create_app(Settings(environment="test"))
    app.dependency_overrides[get_cms_client] = lambda: StubCMSClient(result)
    return TestClient(app)


def test_hospital_endpoint_returns_paginated_live_data_contract() -> None:
    with client_for(hospital_page()) as client:
        response = client.get("/api/v1/hospitals?limit=1&offset=5")

    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 5432
    assert payload["items"][0]["facility_id"] == "010001"
    assert payload["items"][0]["overall_rating"] == 4
    assert payload["source"]["dataset_name"] == "Hospital General Information"


def test_hospital_endpoint_rejects_invalid_pagination() -> None:
    with client_for(hospital_page()) as client:
        response = client.get("/api/v1/hospitals?limit=101&offset=-1")

    assert response.status_code == 422


def test_hospital_endpoint_returns_gateway_timeout_for_slow_cms() -> None:
    with client_for(CMSUpstreamTimeoutError()) as client:
        response = client.get("/api/v1/hospitals?limit=1&offset=5")

    assert response.status_code == 504
    assert "request deadline" in response.json()["detail"]


def test_hospital_endpoint_returns_bad_gateway_for_invalid_cms_data() -> None:
    with client_for(CMSDataError()) as client:
        response = client.get("/api/v1/hospitals?limit=1&offset=5")

    assert response.status_code == 502
    assert "temporarily unavailable" in response.json()["detail"]


def test_openapi_schema_exposes_hospital_endpoint() -> None:
    with client_for(hospital_page()) as client:
        response = client.get("/openapi.json")

    assert response.status_code == 200
    assert "/api/v1/hospitals" in response.json()["paths"]


def test_cms_dependency_builds_client_from_settings() -> None:
    client = get_cms_client(Settings(environment="test"))

    assert isinstance(client, CMSClient)
