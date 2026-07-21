"""Tests for row-level parsing helpers."""

from library_catalogue.library_reader.row_parser import parse_row


def _base_row(**overrides: object) -> dict[str, object]:
    row = {
        "ID": "BK000001",
        "Title": "Dune",
        "Author": "Frank Herbert",
        "Genre": "Science Fiction",
        "Status": "Available",
    }
    row.update(overrides)
    return row


def test_description_literal_backslash_n_becomes_newline() -> None:
    row = _base_row(Description="Line one\\nLine two")
    book = parse_row(row, row_number=1)
    assert book.description == "Line one\nLine two"


def test_description_blank_is_none() -> None:
    row = _base_row(Description="")
    book = parse_row(row, row_number=1)
    assert book.description is None


def test_description_missing_column_is_none() -> None:
    row = _base_row()
    book = parse_row(row, row_number=1)
    assert book.description is None
