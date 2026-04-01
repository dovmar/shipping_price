import logging
import sys


DEFAULT_LOG_LEVEL = 51
APP_LOGGER_NAME = "shipping_price"
LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"


def configure_logging(level: int | None = None) -> None:
    """Configures the shipping_price logger hierarchy.

    Args:
        level (int | None): Optional logging level override. Falls back to INFO.
    """
    resolved_level = level if level is not None else DEFAULT_LOG_LEVEL
    logger = logging.getLogger(APP_LOGGER_NAME)
    logger.setLevel(resolved_level)
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(handler)