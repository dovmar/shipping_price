#  ruff
# Pytest + coverage

import argparse
import logging
from logging import getLogger
from pathlib import Path

from modules.logging_config import APP_LOGGER_NAME, configure_logging
from modules.readers import FileReader, OrdersReader
from modules.rule_applier import RuleApplier
from modules.shipping_options import ShippingOptions, ShippingOptionsReader
from modules.writers import OrdersWriter, STDOUTWriter
from modules.order_rules import rules

_HERE = Path(__file__).parent
LOGGER = getLogger(f"{APP_LOGGER_NAME}.main")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Calculate shipping prices.")
    parser.add_argument(
        "input_file",
        nargs="?",
        help="Input file path (default: input.txt)",
    )
    parser.add_argument(
        "--log-level",
        default=None,
        type=int,
        dest="log_level",
        help="Logging level (default: INFO)",
    )
    return parser.parse_args()


def get_input_path(input_file: str | None) -> Path:
    """Returns the input file path from the CLI or the default input file.

    Returns:
        Path: The path provided as the first script argument (relative to cwd),
            or `input.txt` in the cwd, or `input.txt` beside the script if
            the file doesn't exist in cwd.
    """
    if input_file is not None:
        return Path(input_file)

    cwd_path = Path("input.txt")
    if cwd_path.exists():
        return cwd_path

    return _HERE / "input.txt"



def main() -> None:
    args = parse_args()
    log_level = args.log_level if args.log_level is not None else None
    configure_logging(log_level)

    shipping_options_reader = ShippingOptionsReader()
    shipping_options = ShippingOptions(shipping_options_reader.load_hardcoded_options())

    input_path = get_input_path(args.input_file)
    LOGGER.info("Using input file: %s", input_path)
    file_reader = FileReader(input_path)
    customer_orders_reader = OrdersReader(shipping_options)
    orders, invalid_orders = customer_orders_reader.read_orders_from_file(file_reader)
    LOGGER.info(
        "Loaded %s valid orders and %s invalid orders",
        len(orders),
        len(invalid_orders),
    )

    rule_applier = RuleApplier(rules)
    orders_after_rules = rule_applier.apply_rules(orders, shipping_options)

    std_out_writer = STDOUTWriter()
    orders_writer = OrdersWriter(orders_after_rules, invalid_orders)
    orders_writer.write_orders_to_stdout(std_out_writer)
    LOGGER.info("Finished writing output")


if __name__ == "__main__":
    main()
