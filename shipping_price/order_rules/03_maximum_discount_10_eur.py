from typing import Iterable
from ..modules.order import Order
from ..modules.shipping_options import ShippingOptions

__all__ = ["rule_03_maximum_discount_10_eur"]


def _get_month_key(order: Order) -> str:
    """Builds a year-month key for monthly discount tracking.

    Args:
        order (Order): The order whose date is used for grouping.

    Returns:
        str: The month key in YYYY-MM format.
    """
    return order.order_date.strftime("%Y-%m")


def _calculate_discount(order: Order) -> float:
    """Calculates the currently applied discount for an order.

    Args:
        order (Order): The order with both base `price` and current
            `reduced_price` values.

    Returns:
        float: The non-negative discount applied to the order.
    """
    original_price = order.price
    current_price = order.reduced_price
    return max(0.0, original_price - current_price)


def _apply_discount_cap(
    order: Order,
    discount: float,
    used_discount_for_month: float,
    max_discount: float,
) -> float:
    """Applies the remaining discount budget to a single order.

    Args:
        order (Order): The order being updated.
        discount (float): The discount currently applied to the order.
        used_discount_for_month (float): The cumulative discount already used
            in the order's month.
        max_discount (float): The maximum total discount allowed.

    Returns:
        float: The updated cumulative discount after processing the order.
    """
    allowed_discount = min(discount, max(0.0, max_discount - used_discount_for_month))
    order.reduced_price = order.price - allowed_discount

    return used_discount_for_month + allowed_discount


def rule_03_maximum_discount_10_eur(
    orders: Iterable[Order],
    shipping_options: ShippingOptions,
) -> Iterable[Order]:
    """Caps the accumulated discount per calendar month to 10 EUR.

    Compares each order's current price against its original price to determine
    the applied discount. Once the cumulative discount for a month reaches
    10 EUR, any remaining discount on subsequent orders in that same month is
    reduced so that the monthly total does not exceed the cap.

    Args:
        orders (Iterable[Order]): The orders in their current state, each
            containing both base `price` and mutable `reduced_price` values.
        shipping_options (ShippingOptions): The available shipping options (unused
            by this rule, present for a consistent rule interface).

    Returns:
        Iterable[Order]: The updated orders with prices adjusted so the monthly
            discount does not exceed 10 EUR.
    """
    max_discount = 10.0
    used_discount_by_month: dict[str, float] = {}
    updated_orders: list[Order] = []

    for order in orders:
        month_key = _get_month_key(order)
        used_discount_for_month = used_discount_by_month.get(month_key, 0.0)

        discount = _calculate_discount(order)
        used_discount_by_month[month_key] = _apply_discount_cap(
            order,
            discount,
            used_discount_for_month,
            max_discount,
        )

        updated_orders.append(order)

    return updated_orders
