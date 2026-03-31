import importlib
import inspect
import pkgutil
import sys

# Get the current package
current_package = sys.modules[__name__]
package_path = current_package.__path__

rules = []
_seen = set()

# Dynamically import all modules in alphanumerical order
for _, modname, _ in sorted(pkgutil.iter_modules(package_path), key=lambda item: item[1]):
    module = importlib.import_module(f".{modname}", package=__name__)

    # Use module __all__ if present, otherwise all public names
    names = module.__all__ if hasattr(module, "__all__") else [
        name for name in dir(module) if not name.startswith("_")
    ]

    for name in sorted(names):
        obj = getattr(module, name)
        globals()[name] = obj

        # Keep only functions in rules, no duplicates
        if inspect.isfunction(obj) and obj not in _seen:
            rules.append(obj)
            _seen.add(obj)

# Guarantee deterministic alphanumerical ordering in rules
rules.sort(key=lambda func: (func.__name__.casefold(), func.__module__.casefold()))
