"""Book availability status values."""

from enum import StrEnum


class Status(StrEnum):
    """Valid values for a book's ``Status`` column.

    Kept separate from :class:`~library_catalogue.models.book.Book.status`
    (which stores the raw, possibly-invalid, spreadsheet value) so the
    validator can report bad values instead of rejecting them at parse time.
    """

    AVAILABLE = "Available"
    ON_LOAN = "On Loan"
    RESERVED = "Reserved"

    @classmethod
    def values(cls) -> set[str]:
        return {member.value for member in cls}

    def slug(self) -> str:
        return status_slug(self.value)


def status_slug(status: str) -> str:
    """Convert a status value into a CSS-safe slug, e.g. ``"On Loan"`` -> ``"on-loan"``."""
    return status.strip().lower().replace(" ", "-")
