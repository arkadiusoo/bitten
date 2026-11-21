from app.services.catalog_service import is_variant_available

def test_active_variant_is_available():
    variant_id = "variant-001"
    assert is_variant_available(variant_id) is True

def test_inactive_variant_is_unavailable():
    variant_id = "variant-003"
    assert is_variant_available(variant_id) is False

def test_unknown_variant_is_unavailable():
    variant_id = "variant-999"
    assert is_variant_available(variant_id) is False