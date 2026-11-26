from fastapi import APIRouter, HTTPException, Depends
from collections.abc import AsyncIterator
import httpx
from app.config import Settings

# Configure settings and HTTP client

settings = Settings()

catalog_service_url = str(settings.catalog_service_url)
http_timeout_seconds = float(settings.http_timeout_seconds)

router = APIRouter(
    prefix="/api/v1/health",
    tags=["Health Check"],
)

# Helper functions

async def get_catalog_client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(
        base_url=catalog_service_url, 
        timeout=http_timeout_seconds
        ) as client:
            yield client

# Endpoints

@router.get("", response_model=dict[str, str])
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "listing-service"}

@router.get("/catalog", response_model=dict[str, str])
async def catalog_health_check(
    catalog_client: httpx.AsyncClient = Depends(get_catalog_client)
) -> dict[str, str]:
    try:
        response = await catalog_client.get("api/v1/health")
        print(f"Catalog service health check response: {response.status_code}")
        response.raise_for_status()
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="Catalog service unavailable")
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Catalog service timeout")
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=502, detail=f"Bad Gateway: Catalog service returned an error: {exc.response.status_code}")
        
    return response.json()