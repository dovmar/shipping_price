from pathlib import Path

import pytest

from shipping_price.modules.readers import FileReader, OrdersReader
from shipping_price.modules.shipping_options import ShippingOptions


def test_file_reader_reads_lines(tmp_path: Path) -> None:
    sample = tmp_path / "orders.txt"
    sample.write_text("2015-02-01 S MR\n", encoding="utf-8")

    reader = FileReader(str(sample))

    assert list(reader.read_lines()) == ["2015-02-01 S MR\n"]


def test_orders_reader_parses_valid_and_invalid_lines(
    shipping_options: ShippingOptions,
) -> None:
    orders_reader = OrdersReader(shipping_options)

    lines = [
        "2015-02-01 S MR\n",
        "2015-02-01 SSMR\n",
        "2015-02-02 L LP\n",
    ]

    parsed_orders, invalid_orders = orders_reader.parse_from_lines(lines)

    assert len(parsed_orders) == 2
    assert parsed_orders[0].provider == "MR"
    assert parsed_orders[1].package_size == "L"

    assert len(invalid_orders) == 1
    assert invalid_orders[0].line == "2015-02-01 SSMR"
    assert invalid_orders[0].item_number == 1


def test_orders_reader_raises_when_split_has_more_than_three_items(
    shipping_options: ShippingOptions,
) -> None:
    orders_reader = OrdersReader(shipping_options)
    
    lines = ["2015-02-01 S MR EXTRA\n"]

    with pytest.raises(ValueError, match="Too many items extracted"):
        orders_reader.parse_from_lines(lines)


def test_read_orders_from_file_uses_file_reader(
    tmp_path: Path,
    shipping_options: ShippingOptions,
) -> None:
    sample = tmp_path / "orders.txt"
    sample.write_text("2015-02-01 S MR\ninvalid\n", encoding="utf-8")

    orders_reader = OrdersReader(shipping_options)

    parsed_orders, invalid_orders = orders_reader.read_orders_from_file(
        FileReader(str(sample))
    )

    assert len(parsed_orders) == 1
    assert len(invalid_orders) == 1
