
from typing import Iterable, Union
from .order import Order
from .order import InvalidOrder

class STDOUTWriter:
    """A writer class that outputs data to standard output (stdout).

    This class provides functionality to write lines of text directly
    to the standard output stream.

    Example:
        >>> writer = STDOUTWriter()
        >>> writer.write_to_stdout("Hello, World!")
        Hello, World!
    """

    def __init__(self) -> None:
        """Initializes the STDOUTWriter."""
        pass

    def write_to_stdout(self, line: str) -> None:
        """Writes a line of text to standard output.

        Args:
            line (str): The text to write to stdout.
        """
        print(line)
        
class STDOUTWriter:
    """A writer class that outputs data to standard output (stdout).

    This class provides functionality to write lines of text directly
    to the standard output stream.

    Example:
        >>> writer = STDOUTWriter()
        >>> writer.write_to_stdout("Hello, World!")
        Hello, World!
    """

    def __init__(self) -> None:
        """Initializes the STDOUTWriter."""
        pass

    def write_to_stdout(self, line: str) -> None:
        """Writes a line of text to standard output.

        Args:
            line (str): The text to write to stdout.
        """
        print(line)
class OrdersWriter:
    """Formats and writes processed orders to standard output.

    Attributes:
        _orders (Iterable[Order]): The orders after rule application.
        _orders_original (Iterable[Order]): The original unmodified orders.
    """

    def __init__(self, orders: Iterable[Order], invalid_orders: Iterable[InvalidOrder]) -> None:
        """Initializes the CustomerOrdersWriter.

        Args:
            orders (Iterable[Order]): The orders after rule application.
            orders_original (Iterable[Order]): The original unmodified orders
                used to compute applied discounts.
            invalid_orders (Iterable[InvalidOrder]): The orders that failed validation.
        """
        self._orders = orders
        self._invalid_orders = invalid_orders

    def _build_result_line(self, item: Union[InvalidOrder, Order]) -> str:
        """Formats a single order as an output line with the applied discount.

        Args:
            order (Order): The order after rule application.
            invalid_order (InvalidOrder): The invalid order information.

        Returns:
            str: A formatted string with date, package size, provider, final
                price, and applied discount.

        """
        if isinstance(item, InvalidOrder):
            return f"{item.line} Ignored"

        elif isinstance(item, Order):
            discount = item.price - item.reduced_price
            return f"{item.order_date} {item.package_size} {item.provider} {item.price:.2f} {discount:.2f}"
        
        else:
            raise ValueError("Invalid order type for result line formatting.")

    def _merge_orders(self) -> Iterable[str]:
        """Merges valid and invalid orders into a single iterable"""
        combined = []
        for order in self._orders:
            combined.append(order)

        for invalid_order in self._invalid_orders:
            combined.append(invalid_order)

        combined.sort(key=lambda item: item.item_number)
        return combined

    def write_orders_to_stdout(self, stdout_writer: STDOUTWriter) -> None:
        """Writes all orders to standard output with their applied discounts."""
        merged_orders = self._merge_orders()
        for item in merged_orders:
            result = self._build_result_line(item)
            stdout_writer.write_to_stdout(result)


