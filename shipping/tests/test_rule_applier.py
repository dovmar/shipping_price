from datetime import date

from shipping.modules.order import Order
from shipping.modules.rule_applier import RuleApplier
from shipping.modules.shipping_options import ShippingOptions, ShippingOptionsReader


def _build_order(provider: str = "LP", package_size: str = "S") -> Order:
    shipping_options = ShippingOptions(ShippingOptionsReader().load_hardcoded_options())
    order = Order(date(2015, 2, 1), provider, package_size, 0)
    order.init_price(shipping_options)
    return order


def test_apply_rules_runs_rules_in_order() -> None:
    execution_order: list[str] = []

    def rule_one(orders, shipping_options):
        execution_order.append("rule_one")
        for order in orders:
            order.reduced_price -= 0.10
        return orders

    def rule_two(orders, shipping_options):
        execution_order.append("rule_two")
        for order in orders:
            order.reduced_price -= 0.20
        return orders

    shipping_options = ShippingOptions(ShippingOptionsReader().load_hardcoded_options())
    orders = [_build_order()]

    result = RuleApplier([rule_one, rule_two]).apply_rules(orders, shipping_options)

    assert execution_order == ["rule_one", "rule_two"]
    assert result[0].reduced_price == 1.20
