from datetime import date
from typing import Callable

from shipping_price.modules.order import Order
from shipping_price.modules.shipping_options import (
    ShippingOptions,
)
from shipping_price.order_rules import rule_01_match_the_lowest_S_price_for_each_order


def test_rule_01_sets_s_orders_to_lowest_s_price(
    shipping_options: ShippingOptions,
    build_order: Callable[[date, str, str, int], Order],
) -> None:
    orders = [
        build_order(date(2015, 2, 1), "MR", "S", 0),
        build_order(date(2015, 2, 1), "LP", "M", 1),
    ]

    result = rule_01_match_the_lowest_S_price_for_each_order(orders, shipping_options)

    assert result[0].reduced_price == 1.50
    assert result[1].reduced_price == 4.90
