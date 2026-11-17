from fastapi import FastAPI, HTTPException
from app.config import Settings

from app.schemas import DeviceVariant

settings = Settings()
http_timeout_seconds = float(settings.http_timeout_seconds)

app = FastAPI()


@app.get("/api/v1/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "catalog-service"}

variants = {
    "variant-001": DeviceVariant(
        id="variant-001",
        model="iPhone 15",
        storage_gb=128,
        color="Black",
        active=True,
    ),
    "variant-002": DeviceVariant(
        id="variant-002",
        model="iPhone 15",
        storage_gb=256,
        color="Blue",
        active=True,
    ),
}
@app.get("/api/v1/variants/{variant_id}", response_model=DeviceVariant,
          responses={404: {"description": "Variant not found"}})
def get_variant(variant_id: str) -> DeviceVariant:
    variant = variants.get(variant_id)

    if variant is None:
        raise HTTPException(
            status_code=404,
            detail="Variant not found",
        )

    return variant