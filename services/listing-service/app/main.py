from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "listing-service"}

@app.get("/catalog-health")
async def catalog_health_check() -> dict[str, str]:
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            response = await client.get("http://catalog-service:8000/health")
            response.raise_for_status()
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail="Catalog service unavailable")
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Catalog service timeout")
        
    return response.json()