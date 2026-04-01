from datetime import date

import pytest

from shipping_price.modules.order import Order
from shipping_price.modules.shipping_options import ShippingOptions


def test_init_price_sets_price_and_reduced_price(
    shipping_options: ShippingOptions,
) -> None:
    order = Order(
        order_date=date(2015, 2, 1),
        provider="LP",
        package_size="S",
        item_number=0,
    )

    order.init_price(shipping_options)

    assert order.price == 1.50
    assert order.reduced_price == 1.50


def test_init_price_raises_for_unknown_provider(
    shipping_options: ShippingOptions,
) -> None:
    order = Order(
        order_date=date(2015, 2, 1),
        provider="XX",
        package_size="S",
        item_number=0,
    )

    with pytest.raises(ValueError, match="No shipping option found"):
        order.init_price(shipping_options)
