"""Tests for ValidationIssue / ValidationReport."""

from library_catalogue.models import Severity, ValidationIssue, ValidationReport


def test_errors_and_warnings_split_correctly() -> None:
    report = ValidationReport(
        issues=[
            ValidationIssue(Severity.ERROR, "DUPLICATE_ID", "duplicate", book_id="BK000001"),
            ValidationIssue(Severity.WARNING, "MISSING_COVER", "no cover", book_id="BK000002"),
        ]
    )
    assert len(report.errors) == 1
    assert len(report.warnings) == 1
    assert report.has_errors is True


def test_has_errors_false_when_only_warnings() -> None:
    report = ValidationReport(
        issues=[ValidationIssue(Severity.WARNING, "MISSING_COVER", "no cover", book_id="BK000002")]
    )
    assert report.has_errors is False


def test_summary_lines_includes_counts_and_issues() -> None:
    report = ValidationReport(
        issues=[ValidationIssue(Severity.ERROR, "DUPLICATE_ID", "duplicate", book_id="BK000001")]
    )
    lines = report.summary_lines(book_count=10)
    assert lines[0] == "Validation summary: 10 books, 1 errors, 0 warnings"
    assert "DUPLICATE_ID" in lines[1]
    assert "BK000001" in lines[1]


def test_issue_format_falls_back_to_row_number() -> None:
    issue = ValidationIssue(Severity.ERROR, "MISSING_REQUIRED_FIELD", "title missing", row_number=5)
    assert "row 5" in issue.format()
