from datetime import date
from typing import Callable

import pytest

from shipping_price.modules.order import Order
from shipping_price.modules.rule_applier import RuleApplier
from shipping_price.modules.shipping_options import ShippingOptions


def test_apply_rules_runs_rules_in_order(
    shipping_options: ShippingOptions,
    build_order: Callable[[date, str, str, int], Order],
) -> None:
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

    orders = [build_order(date(2015, 2, 1), "LP", "S", 0)]

    result = RuleApplier([rule_one, rule_two]).apply_rules(orders, shipping_options)

    assert execution_order == ["rule_one", "rule_two"]
    assert result[0].price - result[0].reduced_price == pytest.approx(0.30)
