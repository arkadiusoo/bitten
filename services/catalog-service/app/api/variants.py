from fastapi import APIRouter, HTTPException
from app.repositories.variant_repository import get_variant_by_id
from app.schemas import DeviceVariant

router = APIRouter(
    prefix="/api/v1/variants",
    tags=["Variants"],
)

@router.get("/{variant_id}", response_model=DeviceVariant, 
            responses={404: {"description": "Variant not found"}})
def get_variant(variant_id: str) -> DeviceVariant:
    variant = get_variant_by_id(variant_id)

    if variant is None:
        raise HTTPException(
            status_code=404,
            detail="Variant not found",
        )

    return variant