"""Configures console logging for the CLI."""

import logging


def configure_logging(verbose: bool = False) -> None:
    """Set up a plain, timestamp-free console logger.

    INFO (the default) is what carries the validation summary and build
    summary through to the console; ``--verbose`` drops to DEBUG for
    troubleshooting.
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(message)s", force=True)
