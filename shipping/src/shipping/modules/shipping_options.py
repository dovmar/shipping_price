



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


class ShippingOptions:
    """Manages the available shipping options from all providers.

    Attributes:
        items (Iterable[ShippingOption]): The collection of shipping options.
    """

    def hardcoded_options(self) -> None:
        """Populates the hardcoded shipping options and cached lookup sets."""
        self.items = [
            ShippingOption(Provider="LP", Package_Size="S", Price=1.50),
            ShippingOption(Provider="LP", Package_Size="M", Price=4.90),
            ShippingOption(Provider="LP", Package_Size="L", Price=6.90),
            ShippingOption(Provider="MR", Package_Size="S", Price=2.00),
            ShippingOption(Provider="MR", Package_Size="M", Price=3.00),
            ShippingOption(Provider="MR", Package_Size="L", Price=4.00),
        ]
        self._distinct_providers = frozenset(option.Provider for option in self.items)
        self._distinct_package_sizes = frozenset(option.Package_Size for option in self.items)

    def __init__(self) -> None:
        """Initializes ShippingOptions with hardcoded shipping options."""
        self.items: Iterable[ShippingOption] = None
        self._distinct_providers: frozenset[str] = None
        self._distinct_package_sizes : frozenset[str] = None
    
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
        return True

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
        return True

