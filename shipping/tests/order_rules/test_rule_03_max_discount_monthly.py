from datetime import date

import pytest

from shipping.modules.order import Order
from shipping.modules.shipping_options import ShippingOptions, ShippingOptionsReader
from shipping.order_rules import rule_03_maximum_discount_10_eur


def _build_discounted_order(
    shipping_options: ShippingOptions,
    order_date: date,
    provider: str,
    package_size: str,
    item_number: int,
    reduced_price: float,
) -> Order:
    order = Order(
        order_date=order_date,
        provider=provider,
        package_size=package_size,
        item_number=item_number,
    )
    order.init_price(shipping_options)
    order.reduced_price = reduced_price
    return order


def test_rule_03_applies_partial_discount_when_monthly_cap_hit() -> None:
    shipping_options = ShippingOptions(ShippingOptionsReader().load_hardcoded_options())
    orders = [
        _build_discounted_order(shipping_options, date(2015, 2, 1), "LP", "L", 0, 0.0),
        _build_discounted_order(shipping_options, date(2015, 2, 2), "LP", "L", 1, 0.0),
    ]

    result = rule_03_maximum_discount_10_eur(orders, shipping_options)

    assert result[0].reduced_price == 0.0
    assert result[1].reduced_price == pytest.approx(3.8)


def test_rule_03_resets_discount_cap_per_month() -> None:
    shipping_options = ShippingOptions(ShippingOptionsReader().load_hardcoded_options())
    orders = [
        _build_discounted_order(shipping_options, date(2015, 2, 1), "LP", "L", 0, 0.0),
        _build_discounted_order(shipping_options, date(2015, 2, 2), "LP", "L", 1, 0.0),
        _build_discounted_order(shipping_options, date(2015, 3, 1), "LP", "L", 2, 0.0),
    ]

    result = rule_03_maximum_discount_10_eur(orders, shipping_options)

    assert result[0].reduced_price == 0.0
    assert result[1].reduced_price == pytest.approx(3.8)
    assert result[2].reduced_price == 0.0
