from collections.abc import AsyncIterator

import httpx
from fastapi.testclient import TestClient

from app.api.health_check import get_catalog_client
from app.main import app


def mock_handler(request: httpx.Request) -> httpx.Response:
    assert request.method == "GET"
    assert request.url.path == "/api/v1/health"
    assert request.url.host == "mock-catalog-service"

    return httpx.Response(
        status_code=200,
        json={
            "status": "ok",
            "service": "catalog-service",
        },
    )


async def get_mock_catalog_client() -> AsyncIterator[httpx.AsyncClient]:
    mock_transport = httpx.MockTransport(mock_handler)

    async with httpx.AsyncClient(
        base_url="http://mock-catalog-service",
        transport=mock_transport,
    ) as client:
        yield client


def test_health_check() -> None:
    with TestClient(app) as client:
        response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "listing-service",
    }


def test_catalog_health_check() -> None:
    app.dependency_overrides[get_catalog_client] = get_mock_catalog_client

    try:
        with TestClient(app) as client:
            response = client.get("/api/v1/health/catalog")

        assert response.status_code == 200
        assert response.json() == {
            "status": "ok",
            "service": "catalog-service",
        }

    finally:
        app.dependency_overrides.clear()