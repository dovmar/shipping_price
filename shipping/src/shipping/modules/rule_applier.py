

from typing import Iterable
from .order import Order
from .shipping_options import ShippingOptions

class RuleApplier:
    """Applies a sequence of pricing rules to a collection of orders.

    Attributes:
        rules (Iterable): An ordered collection of rule callables to apply.
    """

    def __init__(self, rules: Iterable) -> None:
        """Initializes the RuleApplier with the given rules.

        Args:
            rules (Iterable): An ordered collection of rule callables. Each rule
                must accept (orders, shipping_options)
                and return an updated iterable of orders.
        """
        self.rules = rules

    def apply_rules(
        self,
        orders: Iterable[Order],
        shipping_options: ShippingOptions,
    ) -> Iterable[Order]:
        """Applies all rules sequentially to the current orders.

        Args:
            orders (Iterable[Order]): The original unmodified orders,
                used by rules that need to compare against initial prices.
            shipping_options (ShippingOptions): The available shipping options
                passed to each rule.

        Returns:
            Iterable[Order]: The orders after all rules have been applied.
        """
        orders_current = orders.copy()
        for rule in self.rules:
            print(f"Applying rule: {rule.__name__}")
            orders_current = rule(orders_current, shipping_options)
            print(orders_current)
        return orders_current
    