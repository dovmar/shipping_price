from datetime import date
from typing import Callable

import pytest

from shipping_price.modules.order import Order
from shipping_price.modules.shipping_options import (
    ShippingOption,
    ShippingOptions,
)


@pytest.fixture
def shipping_option_items() -> list[ShippingOption]:
    """Returns a stable shipping options set for tests.

    Tests should rely on this fixture instead of hardcoded reader output so
    they remain stable if production defaults change.
    """
    return [
        ShippingOption(Provider="LP", Package_Size="S", Price=1.50),
        ShippingOption(Provider="LP", Package_Size="M", Price=4.90),
        ShippingOption(Provider="LP", Package_Size="L", Price=6.90),
        ShippingOption(Provider="MR", Package_Size="S", Price=2.00),
        ShippingOption(Provider="MR", Package_Size="M", Price=3.00),
        ShippingOption(Provider="MR", Package_Size="L", Price=4.00),
    ]


@pytest.fixture
def shipping_options(shipping_option_items: list[ShippingOption]) -> ShippingOptions:
    """Builds ShippingOptions from stable test data."""
    return ShippingOptions(shipping_option_items)


@pytest.fixture
def build_order(
    shipping_options: ShippingOptions,
) -> Callable[[date, str, str, int], Order]:
    """Factory that creates an order and initializes its price."""

    def _build_order(
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

    return _build_order


@pytest.fixture
def build_discounted_order(
    build_order: Callable[[date, str, str, int], Order],
) -> Callable[[date, str, str, int, float], Order]:
    """Factory that creates an initialized order with an overridden reduced price."""

    def _build_discounted_order(
        order_date: date,
        provider: str,
        package_size: str,
        item_number: int,
        reduced_price: float,
    ) -> Order:
        order = build_order(order_date, provider, package_size, item_number)
        order.reduced_price = reduced_price
        return order

    return _build_discounted_order
