from shipping_price.modules.order_rules import rules


def test_rules_collection_contains_expected_rules() -> None:
    rule_names = [rule.__name__ for rule in rules]

    assert "rule_01_match_the_lowest_S_price_for_each_order" in rule_names
    assert "rule_02_third_shippment_via_LP_free" in rule_names
    assert "rule_03_maximum_discount_10_eur" in rule_names


def test_rules_collection_is_sorted_deterministically() -> None:
    rule_names = [rule.__name__ for rule in rules]

    assert rule_names == sorted(rule_names, key=str.casefold)
