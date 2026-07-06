"""Aggregate statistics about the catalogue shown on the index page."""

from collections.abc import Sequence
from dataclasses import dataclass

from library_catalogue.models import Book, Status


@dataclass(frozen=True)
class CatalogueStats:
    total_books: int
    available_count: int
    genres: tuple[str, ...]
    languages: tuple[str, ...]


def compute_stats(books: Sequence[Book]) -> CatalogueStats:
    total_books = len(books)
    available_count = sum(1 for book in books if book.status == Status.AVAILABLE.value)
    genres = tuple(sorted({book.genre for book in books if book.genre}))
    languages = tuple(sorted({book.language for book in books if book.language}))
    return CatalogueStats(
        total_books=total_books,
        available_count=available_count,
        genres=genres,
        languages=languages,
    )
