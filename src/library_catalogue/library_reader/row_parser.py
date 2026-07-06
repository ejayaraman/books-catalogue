"""Converts a single raw spreadsheet row into a Book."""

import logging
from typing import Any

from library_catalogue.models import Book

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = ("ID", "Title", "Author", "Genre", "Status")

OPTIONAL_COLUMNS = (
    "ISBN",
    "Language",
    "Publisher",
    "Publication Year",
    "Shelf",
    "Tags",
    "Notes",
    "Rating",
    "Cover Image",
)

ALL_COLUMNS = REQUIRED_COLUMNS + OPTIONAL_COLUMNS


def _clean_str(value: Any) -> str:
    """Normalize a raw cell value into a stripped string, or "" if blank/NaN."""
    if value is None:
        return ""
    text = str(value).strip()
    if text.lower() == "nan":
        return ""
    return text


def _clean_optional_str(value: Any) -> str | None:
    text = _clean_str(value)
    return text or None


def _clean_optional_int(value: Any, *, row_number: int, field_name: str) -> int | None:
    text = _clean_str(value)
    if not text:
        return None
    try:
        return int(float(text))
    except ValueError:
        logger.warning(
            "Row %d: could not parse %s %r as an integer; ignoring", row_number, field_name, text
        )
        return None


def _parse_tags(value: Any) -> tuple[str, ...]:
    text = _clean_str(value)
    if not text:
        return ()
    return tuple(tag.strip() for tag in text.split(",") if tag.strip())


def parse_row(row: dict[str, Any], row_number: int) -> Book:
    """Build a Book from one raw spreadsheet row.

    Required fields are never rejected here -- a blank required cell becomes
    ``""`` so the validator can report it, rather than the reader raising and
    stopping at the first bad row.
    """
    return Book(
        id=_clean_str(row.get("ID")),
        title=_clean_str(row.get("Title")),
        author=_clean_str(row.get("Author")),
        genre=_clean_str(row.get("Genre")),
        status=_clean_str(row.get("Status")),
        row_number=row_number,
        isbn=_clean_optional_str(row.get("ISBN")),
        language=_clean_optional_str(row.get("Language")),
        publisher=_clean_optional_str(row.get("Publisher")),
        publication_year=_clean_optional_int(
            row.get("Publication Year"), row_number=row_number, field_name="Publication Year"
        ),
        shelf=_clean_optional_str(row.get("Shelf")),
        tags=_parse_tags(row.get("Tags")),
        notes=_clean_optional_str(row.get("Notes")),
        rating=_clean_optional_str(row.get("Rating")),
        cover_image=_clean_optional_str(row.get("Cover Image")),
    )
