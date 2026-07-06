"""Core data model for a single physical book copy."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Book:
    """One row from the spreadsheet, representing one physical copy.

    Required fields are typed ``str`` and default to ``""`` when missing from
    the sheet rather than raising during parsing -- this lets the reader
    always produce a ``Book`` per row so the validator can collect *every*
    problem in one pass instead of stopping at the first bad row. Optional
    fields use ``None`` (never a sentinel empty string) so template
    ``{% if %}`` checks and JSON ``null`` fall out naturally.
    """

    id: str
    title: str
    author: str
    genre: str
    status: str
    row_number: int
    isbn: str | None = None
    language: str | None = None
    publisher: str | None = None
    publication_year: int | None = None
    shelf: str | None = None
    tags: tuple[str, ...] = field(default_factory=tuple)
    notes: str | None = None
    rating: str | None = None
    cover_image: str | None = None
