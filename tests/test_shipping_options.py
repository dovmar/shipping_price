import pytest

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
    with pytest.raises(ValueError, match="Invalid provider"):
        shipping_options.validate_provider("XX")


def test_validate_package_size_raises_for_invalid_size(
    shipping_options: ShippingOptions,
) -> None:
    with pytest.raises(ValueError, match="Invalid package size"):
        shipping_options.validate_package_size("XL")
