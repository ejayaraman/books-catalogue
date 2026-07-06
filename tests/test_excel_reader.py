"""Tests for the spreadsheet reader."""

from pathlib import Path

import pandas as pd
import pytest

from library_catalogue.library_reader import SpreadsheetError, read_spreadsheet


def test_reads_valid_spreadsheet(valid_spreadsheet: Path) -> None:
    books = read_spreadsheet(valid_spreadsheet)
    assert len(books) == 10
    first = books[0]
    assert first.id == "BK000001"
    assert first.title == "Dune"
    assert first.author == "Frank Herbert"
    assert first.status == "Available"
    assert first.row_number == 1
    assert first.tags == ("favorites", "classic")


def test_preserves_row_order(valid_spreadsheet: Path) -> None:
    books = read_spreadsheet(valid_spreadsheet)
    assert [book.row_number for book in books] == list(range(1, 11))
    assert [book.id for book in books] == [f"BK{i:06d}" for i in range(1, 11)]


def test_handles_blank_optional_fields(valid_spreadsheet: Path) -> None:
    books = read_spreadsheet(valid_spreadsheet)
    foundation = next(book for book in books if book.id == "BK000003")
    assert foundation.shelf is None
    assert foundation.notes is None
    assert foundation.rating is None

    neuromancer = next(book for book in books if book.id == "BK000006")
    assert neuromancer.language is None


def test_missing_required_column_raises(tmp_path: Path) -> None:
    frame = pd.DataFrame({"Title": ["Dune"], "Author": ["Frank Herbert"]})
    path = tmp_path / "missing_columns.xlsx"
    frame.to_excel(path, index=False)

    with pytest.raises(SpreadsheetError, match="missing required column"):
        read_spreadsheet(path)


def test_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(SpreadsheetError, match="not found"):
        read_spreadsheet(tmp_path / "does_not_exist.xlsx")


def test_blank_required_field_becomes_empty_string(invalid_spreadsheet: Path) -> None:
    books = read_spreadsheet(invalid_spreadsheet)
    missing_title_book = next(book for book in books if book.row_number == 3)
    assert missing_title_book.title == ""
