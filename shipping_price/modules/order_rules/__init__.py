import importlib
import inspect
import pkgutil
import sys
from collections.abc import Callable, Iterable
from types import ModuleType

from ..order import Order
from ..shipping_options import ShippingOptions

Rule = Callable[[Iterable[Order], ShippingOptions], Iterable[Order]]

# Get the current package
current_package = sys.modules[__name__]
package_path = current_package.__path__

rules: list[Rule] = []
_seen: set[Rule] = set()

# Dynamically import all modules in alphanumerical order
for _module_finder, modname, _is_pkg in sorted(
    pkgutil.iter_modules(package_path), key=lambda item: item[1]
):
    module: ModuleType = importlib.import_module(f".{modname}", package=__name__)

    # Use module __all__ if present, otherwise all public names
    names = (
        module.__all__
        if hasattr(module, "__all__")
        else [name for name in dir(module) if not name.startswith("_")]
    )

    for name in sorted(names):
        obj = getattr(module, name)
        globals()[name] = obj

        # Keep only functions in rules, no duplicates
        if inspect.isfunction(obj):
            rule = obj
            if rule not in _seen:
                rules.append(rule)
                _seen.add(rule)

# Guarantee deterministic alphanumerical ordering in rules
rules.sort(key=lambda func: (func.__name__.casefold(), func.__module__.casefold()))
