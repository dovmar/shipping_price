from datetime import date

import pytest

from shipping.modules.order import Order
from shipping.modules.shipping_options import (
    ShippingOption,
    ShippingOptions,
    ShippingOptionsReader,
)
from shipping.order_rules import rule_01_match_the_lowest_S_price_for_each_order


def _build_order(
    shipping_options: ShippingOptions,
    provider: str,
    package_size: str,
    item_number: int,
) -> Order:
    order = Order(
        order_date=date(2015, 2, 1),
        provider=provider,
        package_size=package_size,
        item_number=item_number,
    )
    order.init_price(shipping_options)
    return order


def test_rule_01_sets_s_orders_to_lowest_s_price() -> None:
    shipping_options = ShippingOptions(ShippingOptionsReader().load_hardcoded_options())
    orders = [
        _build_order(shipping_options, "MR", "S", 0),
        _build_order(shipping_options, "LP", "M", 1),
    ]

    result = rule_01_match_the_lowest_S_price_for_each_order(orders, shipping_options)

    assert result[0].reduced_price == 1.50
    assert result[1].reduced_price == 4.90


def test_rule_01_raises_when_no_s_option_exists() -> None:
    shipping_options = ShippingOptions(
        [
            ShippingOption(Provider="LP", Package_Size="M", Price=4.90),
            ShippingOption(Provider="MR", Package_Size="L", Price=4.00),
        ]
    )
    orders = []

    with pytest.raises(ValueError, match="No shipping option found for package_size=S"):
        rule_01_match_the_lowest_S_price_for_each_order(orders, shipping_options)
