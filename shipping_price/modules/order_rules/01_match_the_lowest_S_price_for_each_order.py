from typing import Iterable

from ..order import Order
from ..shipping_options import ShippingOptions

__all__ = ["rule_01_match_the_lowest_S_price_for_each_order"]


def _get_lowest_s_price(shipping_options: ShippingOptions) -> float:
    """Finds the lowest available price for S-sized packages.

    Args:
        shipping_options (ShippingOptions): The available shipping options.

    Returns:
        float: The lowest available S-sized package price.

    Raises:
        ValueError: If no shipping option with package size S is found.
    """
    lowest_s_option = min(
        (option for option in shipping_options.items if option.Package_Size == "S"),
        key=lambda option: option.Price,
        default=None,
    )
    if lowest_s_option is None:
        raise ValueError("No shipping option found for package_size=S")

    return lowest_s_option.Price


def _apply_lowest_s_price(order: Order, lowest_s_price: float) -> Order:
    """Applies the lowest S-sized package price to a matching order.

    Args:
        order (Order): The order to inspect and possibly update.
        lowest_s_price (float): The lowest available S-sized package price.

    Returns:
        Order: The same order instance, updated when the package size is S.
    """
    if order.package_size == "S":
        order.reduced_price = lowest_s_price

    return order


def rule_01_match_the_lowest_S_price_for_each_order(
    orders: Iterable[Order],
    shipping_options: ShippingOptions,
) -> Iterable[Order]:
    """Sets the price of all S-sized orders to the lowest S price across all providers.

    Args:
        orders (Iterable[Order]): The orders in their current state to be updated.
        shipping_options (ShippingOptions): The available shipping options used to
            determine the lowest S-sized package price.

    Returns:
        Iterable[Order]: The updated orders with S-sized package prices adjusted to
            the lowest available S price.

    Raises:
        ValueError: If no shipping option with package size S is found.
    """
    lowest_s_price = _get_lowest_s_price(shipping_options)
    updated_orders: list[Order] = []

    for order in orders:
        updated_orders.append(_apply_lowest_s_price(order, lowest_s_price))

    return updated_orders
