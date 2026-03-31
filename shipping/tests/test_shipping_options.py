from shipping.modules.shipping_options import (
    ShippingOptions,
    ShippingOptionsReader,
)


def test_load_hardcoded_options_returns_expected_items() -> None:
    reader = ShippingOptionsReader()

    options = list(reader.load_hardcoded_options())

    assert len(options) == 6
    assert any(
        option.Provider == "LP" and option.Package_Size == "S" and option.Price == 1.50
        for option in options
    )


def test_validate_provider_and_package_size_accept_valid_values() -> None:
    reader = ShippingOptionsReader()
    shipping_options = ShippingOptions(reader.load_hardcoded_options())

    shipping_options.validate_provider("LP")
    shipping_options.validate_package_size("M")


def test_validate_provider_raises_for_invalid_provider() -> None:
    reader = ShippingOptionsReader()
    shipping_options = ShippingOptions(reader.load_hardcoded_options())

    try:
        shipping_options.validate_provider("XX")
        assert False, "Expected ValueError for invalid provider"
    except ValueError as exc:
        assert "Invalid provider" in str(exc)


def test_validate_package_size_raises_for_invalid_size() -> None:
    reader = ShippingOptionsReader()
    shipping_options = ShippingOptions(reader.load_hardcoded_options())

    try:
        shipping_options.validate_package_size("XL")
        assert False, "Expected ValueError for invalid package size"
    except ValueError as exc:
        assert "Invalid package size" in str(exc)
