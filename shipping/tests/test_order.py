from datetime import date

from shipping.modules.order import Order
from shipping.modules.shipping_options import ShippingOptions, ShippingOptionsReader


def test_init_price_sets_price_and_reduced_price() -> None:
    shipping_options = ShippingOptions(ShippingOptionsReader().load_hardcoded_options())
    order = Order(
        order_date=date(2015, 2, 1),
        provider="LP",
        package_size="S",
        item_number=0,
    )

    order.init_price(shipping_options)

    assert order.price == 1.50
    assert order.reduced_price == 1.50
