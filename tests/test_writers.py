from datetime import date
from typing import Callable

from shipping_price.modules.order import InvalidOrder, Order
from shipping_price.modules.writers import OrdersWriter


class FakeStdoutWriter:
    def __init__(self) -> None:
        self.lines: list[str] = []

    def write_to_stdout(self, line: str) -> None:
        self.lines.append(line)


def test_build_result_line_for_order_and_invalid_order(
    build_order: Callable[[date, str, str, int], Order],
) -> None:
    order = build_order(date(2015, 2, 1), "LP", "S", 0)
    order.reduced_price = 1.20
    invalid = InvalidOrder(line="invalid input", item_number=1)
    writer = OrdersWriter([order], [invalid])

    valid_line = writer._build_result_line(order)
    invalid_line = writer._build_result_line(invalid)

    assert "2015-02-01 S LP 1.20" in valid_line
    assert valid_line.endswith("0.30")
    assert invalid_line == "invalid input Ignored"


def test_write_orders_to_stdout_writes_merged_sorted_output(
    build_order: Callable[[date, str, str, int], Order],
) -> None:
    order = build_order(date(2015, 2, 1), "LP", "S", 1)
    invalid = InvalidOrder(line="oops", item_number=0)
    writer = OrdersWriter([order], [invalid])
    fake_stdout_writer = FakeStdoutWriter()

    writer.write_orders_to_stdout(fake_stdout_writer)

    assert fake_stdout_writer.lines[0] == "oops Ignored"
    assert "2015-02-01 S LP" in fake_stdout_writer.lines[1]
