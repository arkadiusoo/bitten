from fastapi import FastAPI
from app.api.variants import router as variants_router

app = FastAPI()
app.include_router(variants_router)

@app.get("/api/v1/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "catalog-service"}
