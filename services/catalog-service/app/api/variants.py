from fastapi import APIRouter, HTTPException, Depends
from app.repositories.variant_repository import get_variant_by_id
from app.schemas import DeviceVariant

router = APIRouter(
    prefix="/api/v1/variants",
    tags=["Variants"],
)


def get_catalog_name() -> str:
    return "catalog-service"

@router.get("/metadata", response_model=dict[str, str])
def get_catalog_metadata(
    catalog_name: str = Depends(get_catalog_name),) -> dict[str, str]:
    return {"catalog_name": catalog_name}

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