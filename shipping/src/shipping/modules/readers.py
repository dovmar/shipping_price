



from typing import Iterable
from datetime import date
from .shipping_options import ShippingOptions
from .order import Order
from .order import InvalidOrder

class FileReader:
    """Reads raw lines from a text file.

    Attributes:
        filename (str): The path to the file to read.
    """

    def __init__(self, filename: str) -> None:
        """Initializes the FileReader with the given filename.

        Args:
            filename (str): The path to the file to read.
        """
        self.filename = filename

    def read_lines(self) -> Iterable[str]:
        """Reads all lines from the file.

        Returns:
            Iterable[str]: A list of lines read from the file.
        """
        with open(self.filename, "r") as file:
            lines = file.readlines()
        return lines


class OrdersReader:
    """Reads and parses customer orders from files.

    This class is responsible for reading order data from files and parsing
    individual order lines into Order objects. It handles validation and
    tracks invalid orders that cannot be parsed.

    Attributes:
        _shipping_options (ShippingOptions): The shipping options configuration
            used to create Order instances.
    """

    def __init__(self, shipping_options: ShippingOptions) -> None:
        """Initializes the CustomerOrdersReader.

        Args:
            shipping_options (ShippingOptions): The shipping options configuration
                to be used when creating Order instances.
        """
        self._shipping_options = shipping_options

    def read_orders_from_file(self, file_reader: FileReader) -> tuple[list[tuple[Order, int]], list[tuple[str, int]]]:
        """Reads orders from a file and returns parsed and invalid orders.

        Args:
            file_reader (FileReader): The FileReader instance to read order data from.

        Returns:
            tuple[list[Order], list[InvalidOrder]]: A tuple containing a list of
                successfully parsed Order objects and a list of InvalidOrder objects
                for lines that failed parsing.
        """
        lines = file_reader.read_lines()
        parsed_orders, invalid_orders = self.parse_from_lines(lines)
        return parsed_orders, invalid_orders

    def parse_from_lines(self, lines: Iterable[str]) -> tuple[Iterable[Order], Iterable[InvalidOrder]]:
        """Parses order lines and separates valid from invalid orders.

        Each line is expected to contain space-separated values: date,
        package_size, and provider. Lines are processed sequentially
        and validated.

        Args:
            lines (Iterable[str]): An iterable of strings representing order lines.

        Returns:
            tuple[Iterable[Order], Iterable[InvalidOrder]]: A tuple containing a
                list of successfully parsed Order objects and a list of InvalidOrder
                objects for lines that failed validation.
        """
        parsed_orders: list[tuple[Order, int]] = []
        invalid_orders: list[tuple[str, int]] = []

        # Process each line
        for item_number, line in enumerate(lines):
            try:
                line = line.strip()  # Remove leading/trailing whitespace
                if line:  # Skip empty lines
                    # Split the line into components
                    date_str, package_size, provider = line.split()
                    date_obj = date.fromisoformat(date_str)
                    self._shipping_options.validate_provider(provider)
                    self._shipping_options.validate_package_size(package_size)

                    # Create a Order instance
                    order_shipping = Order(order_date=date_obj, provider=provider, package_size=package_size, item_number=item_number)
                    order_shipping.init_price(self._shipping_options)

                    # Append the instance to the list
                    parsed_orders.append(order_shipping)
            except (ValueError, IndexError):
                invalid_orders.append(InvalidOrder(line=line.strip(), item_number=item_number))

        return parsed_orders, invalid_orders
    
