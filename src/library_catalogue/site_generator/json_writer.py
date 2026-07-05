"""Builds and writes the books.json catalogue file."""

import json
import logging
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from library_catalogue.asset_manager.covers import PLACEHOLDER_NAME
from library_catalogue.models import Book
from library_catalogue.site_generator.context_builder import book_to_dict

logger = logging.getLogger(__name__)


def build_catalogue_json(
    books: Sequence[Book], cover_url_by_book_id: dict[str, str]
) -> list[dict[str, Any]]:
    """Build the list of per-book dicts, in original spreadsheet order.

    Row order is preserved (never re-sorted here) so "recently added" is
    derivable client-side and output stays deterministic run-to-run.
    """
    return [
        book_to_dict(
            book,
            cover_url=cover_url_by_book_id.get(book.id, f"covers/{PLACEHOLDER_NAME}"),
            page_url=f"books/{book.id}.html",
        )
        for book in books
    ]


def write_json(data: list[dict[str, Any]], path: Path) -> Path:
    """Write catalogue data as deterministic, human-readable JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    path.write_text(text, encoding="utf-8")
    logger.info("Wrote %d book(s) to %s", len(data), path)
    return path
