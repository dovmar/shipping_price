from dataclasses import dataclass
from datetime import date
from .shipping_options import ShippingOptions


@dataclass
class Order:
    """Represents a customer shipping order with its computed price.

    Attributes:
        order_date (date): The date the order was placed.
        provider (str): The shipping provider identifier.
        package_size (str): The package size category.
        price (float): The current price after applying discounts/rules.
        item_number (int): The sequential line number from the input file.
    """

    order_date: date
    provider: str
    package_size: str
    price: float
    reduced_price: float
    item_number: int

    def __init__(
        self, order_date: date, provider: str, package_size: str, item_number: int
    ) -> None:
        """Initializes an Order and computes its initial price.

        Args:
            order_date (date): The date the order was placed.
            provider (str): The shipping provider identifier
            package_size (str): The package size category.
            item_number (int): The sequential line number from the input file.

        Raises:
            ValueError: If the provider or package size is invalid, or if no
                matching shipping option is found.
        """
        self.order_date = order_date
        self.provider = provider
        self.package_size = package_size
        self.item_number = item_number
        self.price = None
        self.reduced_price = None

    def init_price(self, shipping_options: ShippingOptions) -> float:
        """Looks up the base price for this order from the shipping options.

        Returns:
            float: The base price for the matching provider and package size.

        Raises:
            ValueError: If no matching shipping option is found.
        """
        for option in shipping_options.items:
            if (
                option.Provider == self.provider
                and option.Package_Size == self.package_size
            ):
                self.price = option.Price
                self.reduced_price = option.Price


@dataclass
class InvalidOrder:
    """Represents an order line that could not be parsed.

    Attributes:
        line (str): The raw line content that failed to parse.
        item_number (int): The sequential line number from the input file.
    """

    line: str
    item_number: int
