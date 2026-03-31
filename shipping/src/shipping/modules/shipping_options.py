from dataclasses import dataclass
from typing import Iterable


@dataclass
class ShippingOption:
    """Represents a shipping option offered by a provider.

    Attributes:
        Provider (str): The shipping provider identifier (e.g., "LP", "MR").
        Package_Size (str): The package size category (e.g., "S", "M", "L").
        Price (float): The base price for this shipping option.
    """

    Provider: str
    Package_Size: str
    Price: float


class ShippingOptionsReader:
    def __init__(self) -> None:
        pass

    def load_hardcoded_options(self) -> Iterable[ShippingOption]:
        """Populates the hardcoded shipping options and cached lookup sets."""

        return [
            ShippingOption(Provider="LP", Package_Size="S", Price=1.50),
            ShippingOption(Provider="LP", Package_Size="M", Price=4.90),
            ShippingOption(Provider="LP", Package_Size="L", Price=6.90),
            ShippingOption(Provider="MR", Package_Size="S", Price=2.00),
            ShippingOption(Provider="MR", Package_Size="M", Price=3.00),
            ShippingOption(Provider="MR", Package_Size="L", Price=4.00),
        ]


class ShippingOptions:
    """Manages the available shipping options from all providers.

    Attributes:
        items (Iterable[ShippingOption]): The collection of shipping options.
    """

    def __init__(self, items: Iterable[ShippingOption]) -> None:
        """
        Initialize a ShippingOptions instance.

        Args:
            items: An iterable collection of ShippingOption objects to be managed.

        Attributes:
            items: Stores the collection of shipping options provided.
            _distinct_providers: Cached set of unique provider names (lazily initialized).
            _distinct_package_sizes: Cached set of unique package sizes (lazily initialized).
        """
        """Initializes ShippingOptions with the given shipping options."""
        self.items: list[ShippingOption] = list(items)
        self._distinct_providers: frozenset[str] = frozenset(
            option.Provider for option in self.items
        )
        self._distinct_package_sizes: frozenset[str] = frozenset(
            option.Package_Size for option in self.items
        )

    def validate_provider(self, provider: str) -> bool:
        """Validates that the given provider exists in the available options.

        Args:
            provider (str): The provider identifier to validate.

        Returns:
            bool: True if the provider is valid.

        Raises:
            ValueError: If the provider is not found in the available options.
        """
        if provider not in self._distinct_providers:
            raise ValueError(f"Invalid provider: {provider}")

    def validate_package_size(self, package_size: str) -> bool:
        """Validates that the given package size exists in the available options.

        Args:
            package_size (str): The package size to validate.

        Returns:
            bool: True if the package size is valid.

        Raises:
            ValueError: If the package size is not found in the available options.
        """
        if package_size not in self._distinct_package_sizes:
            raise ValueError(f"Invalid package size: {package_size}")
