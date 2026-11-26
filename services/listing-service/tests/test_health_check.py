from collections.abc import AsyncIterator, Callable

import httpx
from fastapi.testclient import TestClient

from app.api.health_check import get_catalog_client
from app.main import app

# Dependency factory
def create_mock_catalog_client(handler: Callable[[httpx.Request], httpx.Response]) -> Callable:
    async def get_mock_catalog_client() -> AsyncIterator[httpx.AsyncClient]:
        mock_transport = httpx.MockTransport(handler)

        async with httpx.AsyncClient(
            base_url="http://mock-catalog-service",
            transport=mock_transport,
        ) as client:
            yield client
    return get_mock_catalog_client

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

def mock_error_handler(request: httpx.Request) -> httpx.Response:
    return httpx.Response(
        status_code=500,
        json={
            "status": "error",
            "service": "catalog-service",
        },
    )

def mock_timeout_handler(request: httpx.Request) -> httpx.Response:
    raise httpx.TimeoutException("Request timed out")

def mock_connect_error_handler(request: httpx.Request) -> httpx.Response:
    raise httpx.ConnectError("Connection error")


def test_health_check() -> None:
    with TestClient(app) as client:
        response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "listing-service",
    }


def test_catalog_health_check() -> None:
    app.dependency_overrides[get_catalog_client] = (create_mock_catalog_client(mock_handler))

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

def test_catalog_health_check_error() -> None:
    app.dependency_overrides[get_catalog_client] = (create_mock_catalog_client(mock_error_handler))

    try:
        with TestClient(app) as client:
            response = client.get("/api/v1/health/catalog")

        assert response.status_code == 502
        assert response.json() == {
            "detail": "Bad Gateway: Catalog service returned an error: 500"
        }
    finally:
        app.dependency_overrides.clear()

def test_catalog_health_check_timeout() -> None:
    app.dependency_overrides[get_catalog_client] = (create_mock_catalog_client(mock_timeout_handler))

    try:
        with TestClient(app) as client:
            response = client.get("/api/v1/health/catalog")

        assert response.status_code == 504
        assert response.json() == {
            "detail": "Catalog service timeout"
        }
    finally:
        app.dependency_overrides.clear()

def test_catalog_health_check_connect_error() -> None:
    app.dependency_overrides[get_catalog_client] = (create_mock_catalog_client(mock_connect_error_handler))

    try:
        with TestClient(app) as client:
            response = client.get("/api/v1/health/catalog")

        assert response.status_code == 503
        assert response.json() == {
            "detail": "Catalog service unavailable"
        }
    finally:
        app.dependency_overrides.clear()