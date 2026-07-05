"""Tests for the combined validate() entry point."""

from pathlib import Path

from library_catalogue.library_reader import read_spreadsheet
from library_catalogue.validators import validate


def test_valid_spreadsheet_has_no_errors(valid_spreadsheet: Path, fixture_covers_dir: Path) -> None:
    books = read_spreadsheet(valid_spreadsheet)
    report = validate(books, fixture_covers_dir)
    assert report.has_errors is False
    # Most books have no cover in the fixture covers dir -> warnings expected.
    assert len(report.warnings) > 0


def test_invalid_spreadsheet_has_errors(
    invalid_spreadsheet: Path, fixture_covers_dir: Path
) -> None:
    books = read_spreadsheet(invalid_spreadsheet)
    report = validate(books, fixture_covers_dir)
    assert report.has_errors is True
    codes = {issue.code for issue in report.errors}
    assert "DUPLICATE_ID" in codes
    assert "MISSING_REQUIRED_FIELD" in codes
    assert "INVALID_STATUS" in codes
    warning_codes = {issue.code for issue in report.warnings}
    assert "DUPLICATE_ISBN" in warning_codes
