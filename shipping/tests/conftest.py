import sys
from pathlib import Path

# Ensure tests can import the package from the src layout.
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

SRC_SHIPPING = SRC / "shipping"
if str(SRC_SHIPPING) not in sys.path:
    sys.path.insert(0, str(SRC_SHIPPING))
