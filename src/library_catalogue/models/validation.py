"""Validation issue and report types shared by all validator rules."""

from dataclasses import dataclass, field
from enum import StrEnum


class Severity(StrEnum):
    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True)
class ValidationIssue:
    severity: Severity
    code: str
    message: str
    book_id: str | None = None
    row_number: int | None = None

    def format(self) -> str:
        location = self.book_id or (
            f"row {self.row_number}" if self.row_number is not None else "unknown row"
        )
        return f"{self.severity.value.upper()} [{self.code}] {location}: {self.message}"


@dataclass
class ValidationReport:
    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def errors(self) -> list[ValidationIssue]:
        return [issue for issue in self.issues if issue.severity is Severity.ERROR]

    @property
    def warnings(self) -> list[ValidationIssue]:
        return [issue for issue in self.issues if issue.severity is Severity.WARNING]

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def summary_lines(self, book_count: int) -> list[str]:
        lines = [
            f"Validation summary: {book_count} books, "
            f"{len(self.errors)} errors, {len(self.warnings)} warnings"
        ]
        for issue in self.errors + self.warnings:
            lines.append(f"  {issue.format()}")
        return lines
