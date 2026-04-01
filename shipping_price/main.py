#  ruff
# Pytest + coverage

import sys
from pathlib import Path

from modules.readers import FileReader, OrdersReader
from modules.rule_applier import RuleApplier
from modules.shipping_options import ShippingOptions, ShippingOptionsReader
from modules.writers import OrdersWriter, STDOUTWriter
from order_rules import rules

_HERE = Path(__file__).parent


def get_input_path() -> Path:
    """Returns the input file path from the CLI or the default input file.

    Returns:
        Path: The path provided as the first script argument (relative to cwd),
            or `input.txt` in the cwd, or `input.txt` beside the script if
            the file doesn't exist in cwd.
    """
    if len(sys.argv) > 1:
        return Path(sys.argv[1])

    cwd_path = Path("input.txt")
    if cwd_path.exists():
        return cwd_path

    script_path = _HERE / "input.txt"
    return script_path


def main() -> None:
    shipping_options_reader = ShippingOptionsReader()
    shipping_options = ShippingOptions(shipping_options_reader.load_hardcoded_options())

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
