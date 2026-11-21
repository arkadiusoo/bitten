from app.schemas import DeviceVariant

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
    "variant-003": DeviceVariant(
        id="variant-003",
        model="iPhone 15",
        storage_gb=512,
        color="Red",
        active=False,
    ),
}

def get_variant_by_id(variant_id: str) -> DeviceVariant | None:
    return variants.get(variant_id)