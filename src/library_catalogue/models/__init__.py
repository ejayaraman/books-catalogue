"""Data model types shared across the library catalogue generator."""

from library_catalogue.models.book import Book
from library_catalogue.models.build import BuildConfig, BuildSummary
from library_catalogue.models.status import Status, status_slug
from library_catalogue.models.validation import Severity, ValidationIssue, ValidationReport

__all__ = [
    "Book",
    "BuildConfig",
    "BuildSummary",
    "Status",
    "status_slug",
    "Severity",
    "ValidationIssue",
    "ValidationReport",
]
