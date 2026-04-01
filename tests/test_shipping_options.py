from shipping_price.modules.shipping_options import (
    ShippingOptions,
)


def test_load_hardcoded_options_returns_expected_items(
    shipping_options: ShippingOptions,
) -> None:
    options = shipping_options.items

    assert len(options) > 0
    assert all(hasattr(option, "Provider") for option in options)
    assert all(hasattr(option, "Package_Size") for option in options)
    assert all(hasattr(option, "Price") for option in options)


def test_validate_provider_and_package_size_accept_valid_values(
    shipping_options: ShippingOptions,
) -> None:

    shipping_options.validate_provider("LP")
    shipping_options.validate_package_size("M")


def test_validate_provider_raises_for_invalid_provider(
    shipping_options: ShippingOptions,
) -> None:
    try:
        shipping_options.validate_provider("XX")
        assert False, "Expected ValueError for invalid provider"
    except ValueError as exc:
        assert "Invalid provider" in str(exc)


def test_validate_package_size_raises_for_invalid_size(
    shipping_options: ShippingOptions,
) -> None:
    try:
        shipping_options.validate_package_size("XL")
        assert False, "Expected ValueError for invalid package size"
    except ValueError as exc:
        assert "Invalid package size" in str(exc)
