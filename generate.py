"""Entry point: regenerates the entire library catalogue website.

Usage:
    python generate.py
    python generate.py --data data/books.xlsx --output output --verbose
"""

import argparse
import logging
from collections.abc import Sequence
from dataclasses import replace
from pathlib import Path

from library_catalogue.library_reader import SpreadsheetError
from library_catalogue.logging_config import configure_logging
from library_catalogue.models import BuildConfig
from library_catalogue.site_generator import BuildAbortedError, run_build

logger = logging.getLogger(__name__)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=None, help="Path to the books spreadsheet")
    parser.add_argument("--output", type=Path, default=None, help="Output directory")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    configure_logging(args.verbose)

    config = BuildConfig.default()
    if args.data is not None:
        config = replace(config, spreadsheet_path=args.data)
    if args.output is not None:
        config = replace(config, output_dir=args.output)

    try:
        run_build(config)
    except SpreadsheetError as exc:
        logger.error(str(exc))
        return 1
    except BuildAbortedError:
        logger.error("Build aborted: fix the errors above and run again.")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
