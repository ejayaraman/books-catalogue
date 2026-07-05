"""Reads the book spreadsheet into a list of Book objects."""

import logging
from pathlib import Path

import pandas as pd

from library_catalogue.library_reader.row_parser import REQUIRED_COLUMNS, parse_row
from library_catalogue.models import Book

logger = logging.getLogger(__name__)


class SpreadsheetError(Exception):
    """Raised when the spreadsheet cannot be read or is missing required columns."""


def read_spreadsheet(path: Path) -> list[Book]:
    """Read every row of the spreadsheet at ``path`` into a list of Book objects.

    Row order is preserved exactly as it appears in the sheet -- this is what
    drives the "recently added" sort and keeps generation deterministic.
    """
    if not path.exists():
        raise SpreadsheetError(f"Spreadsheet not found: {path}")

    try:
        frame = pd.read_excel(path, dtype=object)
    except Exception as exc:  # pragma: no cover - defensive, pandas raises many types
        raise SpreadsheetError(f"Could not read spreadsheet {path}: {exc}") from exc

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing_columns:
        raise SpreadsheetError(
            f"Spreadsheet {path} is missing required column(s): {', '.join(missing_columns)}"
        )

    books: list[Book] = []
    for offset, row in enumerate(frame.to_dict(orient="records")):
        row_number = offset + 1
        books.append(parse_row(row, row_number))

    logger.info("Read %d book(s) from %s", len(books), path)
    return books
