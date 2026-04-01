from datetime import date
from typing import Callable

import pytest

from shipping_price.modules.order import Order
from shipping_price.modules.shipping_options import ShippingOptions
from shipping_price.order_rules import rule_03_maximum_discount_10_eur


def test_rule_03_applies_partial_discount_when_monthly_cap_hit(
    shipping_options: ShippingOptions,
    build_discounted_order: Callable[[date, str, str, int, float], Order],
) -> None:
    orders = [
        build_discounted_order(date(2015, 2, 1), "LP", "L", 0, 0.0),
        build_discounted_order(date(2015, 2, 2), "LP", "L", 1, 0.0),
    ]

    result = rule_03_maximum_discount_10_eur(orders, shipping_options)

    assert result[0].reduced_price == 0.0
    assert result[1].reduced_price == pytest.approx(3.8)


def test_rule_03_resets_discount_cap_per_month(
    shipping_options: ShippingOptions,
    build_discounted_order: Callable[[date, str, str, int, float], Order],
) -> None:
    orders = [
        build_discounted_order(date(2015, 2, 1), "LP", "L", 0, 0.0),
        build_discounted_order(date(2015, 2, 2), "LP", "L", 1, 0.0),
        build_discounted_order(date(2015, 3, 1), "LP", "L", 2, 0.0),
    ]

    result = rule_03_maximum_discount_10_eur(orders, shipping_options)

    assert result[0].reduced_price == 0.0
    assert result[1].reduced_price == pytest.approx(3.8)
    assert result[2].reduced_price == 0.0
