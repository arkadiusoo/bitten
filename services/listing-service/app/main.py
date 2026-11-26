from fastapi import FastAPI, HTTPException
import httpx
from app.config import Settings

settings = Settings()

catalog_service_url = str(settings.catalog_service_url)
http_timeout_seconds = float(settings.http_timeout_seconds)

app = FastAPI()


@app.get("/api/v1/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "listing-service"}

@app.get("/api/v1/catalog-health")
async def catalog_health_check() -> dict[str, str]:
    async with httpx.AsyncClient(timeout=http_timeout_seconds, base_url=catalog_service_url) as client:
        try:
            response = await client.get("api/v1/health")
            response.raise_for_status()
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail="Catalog service unavailable")
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Catalog service timeout")
        except httpx.HTTPStatusError:
            raise HTTPException(status_code=404, detail="Catalog service not found")
        
    return response.json()