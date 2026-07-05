"""Individual, independently-testable validation rules.

Each function takes the full list of books (and any extra context it needs)
and returns the list of issues it found -- ``validator.validate`` simply
concatenates all of them.
"""

from collections import defaultdict
from collections.abc import Sequence
from pathlib import Path

from library_catalogue.asset_manager.covers import resolve_cover_path
from library_catalogue.models import Book, Severity, Status, ValidationIssue

REQUIRED_FIELDS = ("id", "title", "author", "genre", "status")


def check_required_fields(books: Sequence[Book]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for book in books:
        for field_name in REQUIRED_FIELDS:
            if not getattr(book, field_name):
                issues.append(
                    ValidationIssue(
                        severity=Severity.ERROR,
                        code="MISSING_REQUIRED_FIELD",
                        message=f"required field '{field_name}' is missing",
                        book_id=book.id or None,
                        row_number=book.row_number,
                    )
                )
    return issues


def check_duplicate_ids(books: Sequence[Book]) -> list[ValidationIssue]:
    rows_by_id: dict[str, list[int]] = defaultdict(list)
    for book in books:
        if book.id:
            rows_by_id[book.id].append(book.row_number)

    issues: list[ValidationIssue] = []
    for book_id, rows in sorted(rows_by_id.items()):
        if len(rows) > 1:
            issues.append(
                ValidationIssue(
                    severity=Severity.ERROR,
                    code="DUPLICATE_ID",
                    message=f"ID appears {len(rows)} times, in rows {rows}",
                    book_id=book_id,
                )
            )
    return issues


def check_valid_status(books: Sequence[Book]) -> list[ValidationIssue]:
    valid_values = Status.values()
    issues: list[ValidationIssue] = []
    for book in books:
        if book.status and book.status not in valid_values:
            issues.append(
                ValidationIssue(
                    severity=Severity.ERROR,
                    code="INVALID_STATUS",
                    message=f"status {book.status!r} is not one of {sorted(valid_values)}",
                    book_id=book.id or None,
                    row_number=book.row_number,
                )
            )
    return issues


def check_duplicate_isbns(books: Sequence[Book]) -> list[ValidationIssue]:
    rows_by_isbn: dict[str, list[str]] = defaultdict(list)
    for book in books:
        if book.isbn:
            rows_by_isbn[book.isbn].append(book.id)

    issues: list[ValidationIssue] = []
    for isbn, book_ids in sorted(rows_by_isbn.items()):
        if len(book_ids) > 1:
            issues.append(
                ValidationIssue(
                    severity=Severity.WARNING,
                    code="DUPLICATE_ISBN",
                    message=f"ISBN {isbn} is shared with {sorted(book_ids)}",
                    book_id=book_ids[0],
                )
            )
    return issues


def check_missing_covers(books: Sequence[Book], covers_dir: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for book in books:
        if not book.id:
            continue
        if resolve_cover_path(book, covers_dir) is None:
            issues.append(
                ValidationIssue(
                    severity=Severity.WARNING,
                    code="MISSING_COVER",
                    message="no cover image found; a placeholder will be used",
                    book_id=book.id,
                )
            )
    return issues
