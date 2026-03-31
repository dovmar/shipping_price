#  ruff
# Pytest + coverage

import sys
from pathlib import Path
from modules.shipping_options import ShippingOptions
from modules.readers import OrdersReader, FileReader
from modules.rule_applier import RuleApplier
from modules.writers import OrdersWriter, STDOUTWriter
from order_rules import rules


def get_input_path() -> Path:
    """Returns the input file path from the CLI or the default input file.

    Returns:
        Path: The path provided as the first script argument, or `input.txt`
            in the current working directory when no argument is supplied.
    """
    if len(sys.argv) > 1:
        return Path(sys.argv[1])

    return Path("input.txt")


def main():
    shipping_options = ShippingOptions()
    shipping_options.load_hardcoded_options()
    input_path = get_input_path()
    file_reader = FileReader(input_path)
    customer_orders_reader = OrdersReader(shipping_options)
    orders, invalid_orders = customer_orders_reader.read_orders_from_file(file_reader)

    rule_applier = RuleApplier(rules)
    orders_after_rules = rule_applier.apply_rules(orders, shipping_options)

    std_out_writer = STDOUTWriter()
    orders_writer = OrdersWriter(orders_after_rules, invalid_orders)
    orders_writer.write_orders_to_stdout(std_out_writer)

if __name__ == "__main__":
    main()
