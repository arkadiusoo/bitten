from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/api/v1/health",
    tags=["Health Check"],
)

@router.get("/", response_model=dict[str, str])
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "catalog-service"}
