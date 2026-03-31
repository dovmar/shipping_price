from datetime import date

from shipping.modules.order import Order
from shipping.modules.shipping_options import ShippingOptions, ShippingOptionsReader
from shipping.order_rules import rule_02_third_shippment_via_LP_free


def _build_order(
    shipping_options: ShippingOptions,
    order_date: date,
    provider: str,
    package_size: str,
    item_number: int,
) -> Order:
    order = Order(
        order_date=order_date,
        provider=provider,
        package_size=package_size,
        item_number=item_number,
    )
    order.init_price(shipping_options)
    return order


def test_rule_02_only_third_lp_l_in_month_is_free() -> None:
    shipping_options = ShippingOptions(ShippingOptionsReader().load_hardcoded_options())
    orders = [
        _build_order(shipping_options, date(2015, 2, 1), "LP", "L", 0),
        _build_order(shipping_options, date(2015, 2, 2), "LP", "S", 1),
        _build_order(shipping_options, date(2015, 2, 3), "LP", "L", 2),
        _build_order(shipping_options, date(2015, 2, 4), "MR", "L", 3),
        _build_order(shipping_options, date(2015, 2, 5), "LP", "L", 4),
        _build_order(shipping_options, date(2015, 2, 6), "LP", "L", 5),
    ]

    result = rule_02_third_shippment_via_LP_free(orders, shipping_options)

    assert result[0].reduced_price == 6.90
    assert result[1].reduced_price == 1.50
    assert result[2].reduced_price == 6.90
    assert result[3].reduced_price == 4.00
    assert result[4].reduced_price == 0.0
    assert result[5].reduced_price == 6.90
