# Shipping Price

A Python application for processing shipping orders and applying discount rules.

## Requirements

- Python `3.13` (pinned)
- `uv`

## Environment Setup

```bash
# Install uv (if needed)
python -m pip install uv
```

## Run

```bash
cd shipping_price
uv run python main.py

# Or pass an explicit input file
cd shipping_price
uv run python main.py path/to/input.txt
```

## Tests

```bash
uv run pytest 
```

## Coverage

```bash
# Terminal coverage summary with missing lines
uv run pytest --cov=shipping_price

# HTML report
uv run pytest --cov=shipping_price --cov-report=html
```


## Lint And Format

```bash
# Lint
uv run ruff check .

# Format
uv run ruff format .
```
