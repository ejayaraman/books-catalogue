"""Reads the book CSV file into a list of Book objects."""

import csv
import logging
from pathlib import Path

from library_catalogue.library_reader.row_parser import REQUIRED_COLUMNS, parse_row
from library_catalogue.models import Book

logger = logging.getLogger(__name__)


class SpreadsheetError(Exception):
    """Raised when the CSV file cannot be read or is missing required columns."""


def read_spreadsheet(path: Path) -> list[Book]:
    """Read every row of the CSV file at ``path`` into a list of Book objects.

    Row order is preserved exactly as it appears in the file -- this is what
    drives the "recently added" sort and keeps generation deterministic.
    """
    if not path.exists():
        raise SpreadsheetError(f"Spreadsheet not found: {path}")

    try:
        with path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            fieldnames = reader.fieldnames or []
            missing_columns = [column for column in REQUIRED_COLUMNS if column not in fieldnames]
            if missing_columns:
                raise SpreadsheetError(
                    f"Spreadsheet {path} is missing required column(s): "
                    f"{', '.join(missing_columns)}"
                )

            books: list[Book] = []
            for offset, row in enumerate(reader):
                row_number = offset + 1
                books.append(parse_row(row, row_number))
    except OSError as exc:
        raise SpreadsheetError(f"Could not read spreadsheet {path}: {exc}") from exc

    logger.info("Read %d book(s) from %s", len(books), path)
    return books
