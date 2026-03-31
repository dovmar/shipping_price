from typing import Iterable
from modules.order import Order
from modules.shipping_options import ShippingOptions

__all__ = ["rule_03_maximum_discount_10_eur"]


def _calculate_discount(order: Order) -> float:
    """Calculates the currently applied discount for an order.

    Args:
        order (Order): The order with both base `price` and current
            `reduced_price` values.

    Returns:
        float: The non-negative discount applied to the order.
    """
    original_price = float(order.price)
    current_price = float(order.reduced_price)
    return max(0.0, original_price - current_price)


def _apply_discount_cap(
    order: Order,
    discount: float,
    used_discount: float,
    max_discount: float,
) -> float:
    """Applies the remaining discount budget to a single order.

    Args:
        order (Order): The order being updated.
        discount (float): The discount currently applied to the order.
        used_discount (float): The cumulative discount already used.
        max_discount (float): The maximum total discount allowed.

    Returns:
        float: The updated cumulative discount after processing the order.
    """
    if used_discount + discount > max_discount:
        remaining_discount = max(0.0, max_discount - used_discount)
        order.reduced_price = order.price - remaining_discount
        return max_discount

    return used_discount + discount


def rule_03_maximum_discount_10_eur(
    orders: Iterable[Order],
    shipping_options: ShippingOptions,
) -> Iterable[Order]:
    """Caps the total accumulated discount across all orders to 10 EUR.

    Compares each order's current price against its original price to determine
    the applied discount. Once the cumulative discount reaches 10 EUR, any
    remaining discount on subsequent orders is reduced so that the total does
    not exceed the cap.

    Args:
        orders (Iterable[Order]): The orders in their current state, each
            containing both base `price` and mutable `reduced_price` values.
        shipping_options (ShippingOptions): The available shipping options (unused
            by this rule, present for a consistent rule interface).

    Returns:
        Iterable[Order]: The updated orders with prices adjusted so the total
            discount does not exceed 10 EUR.
    """
    max_discount = 10.0
    used_discount = 0.0
    updated_orders: list[Order] = []

    for order in orders:
        discount = _calculate_discount(order)
        used_discount = _apply_discount_cap(
            order,
            discount,
            used_discount,
            max_discount,
        )

        updated_orders.append(order)

    return updated_orders