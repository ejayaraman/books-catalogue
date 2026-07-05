"""Runs all validation rules and produces a single report."""

from collections.abc import Sequence
from pathlib import Path

from library_catalogue.models import Book, ValidationReport
from library_catalogue.validators.rules import (
    check_duplicate_ids,
    check_duplicate_isbns,
    check_missing_covers,
    check_required_fields,
    check_valid_status,
)


def validate(books: Sequence[Book], covers_dir: Path) -> ValidationReport:
    """Run every validation rule and collect the results into one report."""
    issues = [
        *check_required_fields(books),
        *check_duplicate_ids(books),
        *check_valid_status(books),
        *check_duplicate_isbns(books),
        *check_missing_covers(books, covers_dir),
    ]
    return ValidationReport(issues=issues)
