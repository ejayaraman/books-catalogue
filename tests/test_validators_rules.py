"""Tests for individual validation rules."""

from pathlib import Path

from library_catalogue.models import Book, Severity
from library_catalogue.validators.rules import (
    check_duplicate_ids,
    check_duplicate_isbns,
    check_missing_covers,
    check_required_fields,
    check_valid_status,
)


def make_book(**overrides: object) -> Book:
    defaults = dict(
        id="BK000001",
        title="Dune",
        author="Frank Herbert",
        genre="Science Fiction",
        status="Available",
        row_number=1,
    )
    defaults.update(overrides)
    return Book(**defaults)  # type: ignore[arg-type]


def test_check_required_fields_flags_missing_title() -> None:
    book = make_book(title="")
    issues = check_required_fields([book])
    assert len(issues) == 1
    assert issues[0].code == "MISSING_REQUIRED_FIELD"
    assert issues[0].severity is Severity.ERROR
    assert "title" in issues[0].message


def test_check_required_fields_passes_when_all_present() -> None:
    assert check_required_fields([make_book()]) == []


def test_check_duplicate_ids_flags_shared_id() -> None:
    books = [
        make_book(id="BK000001", row_number=1),
        make_book(id="BK000001", row_number=2),
        make_book(id="BK000002", row_number=3),
    ]
    issues = check_duplicate_ids(books)
    assert len(issues) == 1
    assert issues[0].severity is Severity.ERROR
    assert issues[0].book_id == "BK000001"


def test_check_duplicate_ids_ignores_blank_ids() -> None:
    books = [make_book(id="", row_number=1), make_book(id="", row_number=2)]
    assert check_duplicate_ids(books) == []


def test_check_valid_status_flags_bad_value() -> None:
    issues = check_valid_status([make_book(status="Checked Out")])
    assert len(issues) == 1
    assert issues[0].severity is Severity.ERROR
    assert issues[0].code == "INVALID_STATUS"


def test_check_valid_status_accepts_all_defined_values() -> None:
    for status in ("Available", "On Loan", "Reserved"):
        assert check_valid_status([make_book(status=status)]) == []


def test_check_duplicate_isbns_is_warning_not_error() -> None:
    books = [
        make_book(id="BK000001", isbn="111"),
        make_book(id="BK000002", isbn="111"),
    ]
    issues = check_duplicate_isbns(books)
    assert len(issues) == 1
    assert issues[0].severity is Severity.WARNING
    assert issues[0].code == "DUPLICATE_ISBN"


def test_check_duplicate_isbns_ignores_blank_isbns() -> None:
    books = [make_book(id="BK000001", isbn=None), make_book(id="BK000002", isbn=None)]
    assert check_duplicate_isbns(books) == []


def test_check_missing_covers_is_warning_not_error(tmp_path: Path) -> None:
    covers_dir = tmp_path / "covers"
    covers_dir.mkdir()
    issues = check_missing_covers([make_book(id="BK000001")], covers_dir)
    assert len(issues) == 1
    assert issues[0].severity is Severity.WARNING
    assert issues[0].code == "MISSING_COVER"


def test_check_missing_covers_finds_existing_cover(tmp_path: Path) -> None:
    covers_dir = tmp_path / "covers"
    covers_dir.mkdir()
    (covers_dir / "BK000001.jpg").write_bytes(b"fake-image-bytes")
    assert check_missing_covers([make_book(id="BK000001")], covers_dir) == []
