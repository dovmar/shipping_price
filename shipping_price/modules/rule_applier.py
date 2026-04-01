import logging
from typing import Callable, Iterable

from .order import Order
from .shipping_options import ShippingOptions


LOGGER = logging.getLogger("shipping_price.modules.rule_applier")

Rule = Callable[[Iterable[Order], ShippingOptions], Iterable[Order]]


class RuleApplier:
    """Applies a sequence of pricing rules to a collection of orders.

    Attributes:
        rules (Iterable): An ordered collection of rule callables to apply.
    """

    def __init__(self, rules: Iterable[Rule]) -> None:
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
    ) -> list[Order]:
        """Applies all rules sequentially to the current orders.

        Args:
            orders (Iterable[Order]): The orders to process.
            shipping_options (ShippingOptions): The available shipping options
                passed to each rule.

        Returns:
            list[Order]: The orders after all rules have been applied.
        """
        orders_current = list(orders)
        for rule in self.rules:
            LOGGER.info("Applying rule: %s", rule.__name__)
            orders_current = list(rule(orders_current, shipping_options))
        return orders_current
