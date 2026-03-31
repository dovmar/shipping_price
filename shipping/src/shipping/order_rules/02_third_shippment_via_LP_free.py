from typing import Iterable
from modules.order import Order
from modules.shipping_options import ShippingOptions

__all__ = ["rule_02_third_shippment_via_LP_free"]

def _get_month_key(order: Order) -> str:
    """Builds the year-month key used for monthly LP shipment tracking.

    Args:
        order (Order): The order whose date is used to build the month key.

    Returns:
        str: The month key in YYYY-MM format.
    """
    return order.order_date.strftime("%Y-%m")


def _should_make_lp_shipment_free(
    order: Order,
    month_key: str,
    lp_count_by_month: dict[str, int],
    free_applied_by_month: set[str],
) -> bool:
    """Determines whether the current order qualifies for the LP free shipment rule.

    Args:
        order (Order): The order being evaluated.
        month_key (str): The year-month key for the order date.
        lp_count_by_month (dict[str, int]): LP shipment counts grouped by month.
        free_applied_by_month (set[str]): Months where the free shipment has
            already been applied.

    Returns:
        bool: True if the order is the third LP shipment for its month and the
            free shipment has not already been applied for that month.
    """
    if order.provider != "LP":
        return False

    lp_count_by_month[month_key] = lp_count_by_month.get(month_key, 0) + 1
    return lp_count_by_month[month_key] == 3 and month_key not in free_applied_by_month


def rule_02_third_shippment_via_LP_free(
    orders: Iterable[Order],
    shipping_options: ShippingOptions,
) -> Iterable[Order]:
    """Makes the third LP shipment in each calendar month free of charge.

    Only the first occurrence of the third LP shipment per month is made free.
    Subsequent LP shipments beyond the third in the same month are not affected.

    Args:
        orders (Iterable[Order]): The orders in their current state to be updated.
        shipping_options (ShippingOptions): The available shipping options (unused by
            this rule, present for a consistent rule interface).

    Returns:
        Iterable[Order]: The updated orders with the third LP shipment per month
            set to a price of 0.00.
    """
    lp_count_by_month: dict[str, int] = {}
    free_applied_by_month: set[str] = set()
    updated_orders: list[Order] = []

    for order in orders:
        month_key = _get_month_key(order)

        if _should_make_lp_shipment_free(
            order,
            month_key,
            lp_count_by_month,
            free_applied_by_month,
        ):
            order.reduced_price = 0.0
            free_applied_by_month.add(month_key)

        updated_orders.append(order)

    return updated_orders
