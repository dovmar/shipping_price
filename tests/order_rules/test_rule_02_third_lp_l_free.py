from datetime import date
from typing import Callable

from shipping_price.modules.order import Order
from shipping_price.modules.shipping_options import ShippingOptions
from shipping_price.modules.order_rules import rule_02_third_shippment_via_LP_free


def test_rule_02_only_third_lp_l_in_month_is_free(
    shipping_options: ShippingOptions,
    build_order: Callable[[date, str, str, int], Order],
) -> None:
    orders = [
        build_order(date(2015, 2, 1), "LP", "L", 0),
        build_order(date(2015, 2, 2), "LP", "S", 1),
        build_order(date(2015, 2, 3), "LP", "L", 2),
        build_order(date(2015, 2, 4), "MR", "L", 3),
        build_order(date(2015, 2, 5), "LP", "L", 4),
        build_order(date(2015, 2, 6), "LP", "L", 5),
    ]

    result = rule_02_third_shippment_via_LP_free(orders, shipping_options)

    assert result[0].reduced_price == 6.90
    assert result[1].reduced_price == 1.50
    assert result[2].reduced_price == 6.90
    assert result[3].reduced_price == 4.00
    assert result[4].reduced_price == 0.0
    assert result[5].reduced_price == 6.90


def test_rule_02_resets_free_shipment_on_new_month(
    shipping_options: ShippingOptions,
    build_order: Callable[[date, str, str, int], Order],
) -> None:
    orders = [
        build_order(date(2015, 2, 1), "LP", "L", 0),
        build_order(date(2015, 2, 2), "LP", "L", 1),
        build_order(date(2015, 2, 3), "LP", "L", 2),
        build_order(date(2015, 3, 1), "LP", "L", 3),
        build_order(date(2015, 3, 2), "LP", "L", 4),
        build_order(date(2015, 3, 3), "LP", "L", 5),
    ]

    result = rule_02_third_shippment_via_LP_free(orders, shipping_options)

    assert result[0].reduced_price == 6.90
    assert result[1].reduced_price == 6.90
    assert result[2].reduced_price == 0.0
    assert result[3].reduced_price == 6.90
    assert result[4].reduced_price == 6.90
    assert result[5].reduced_price == 0.0
