from app.repositories.variant_repository import get_variant_by_id

def is_variant_available(variant_id: str) -> bool:
    variant = get_variant_by_id(variant_id)

    if variant is None:
        return False

    return variant.active