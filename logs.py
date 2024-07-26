"""Helper script for logging functions."""

import logging

logging.basicConfig(
    level=logging.NOTSET,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

# Shorthand function names for logging messages.
debug = logging.debug
info = logging.info
warning = logging.warning
error = logging.error