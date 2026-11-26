from fastapi import APIRouter, HTTPException
import httpx
from app.config import Settings

settings = Settings()

catalog_service_url = str(settings.catalog_service_url)
http_timeout_seconds = float(settings.http_timeout_seconds)

router = APIRouter(
    prefix="/api/v1/health",
    tags=["Health Check"],
)

@router.get("/", response_model=dict[str, str])
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "listing-service"}

@router.get("/catalog", response_model=dict[str, str])
async def catalog_health_check() -> dict[str, str]:
    async with httpx.AsyncClient(timeout=http_timeout_seconds, base_url=catalog_service_url) as client:
        try:
            response = await client.get("api/v1/health/")
            response.raise_for_status()
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail="Catalog service unavailable")
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Catalog service timeout")
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=502, detail=f"Bad Gateway: Catalog service returned an error: {exc.response.status_code}")
        
    return response.json()