"""Tests for CatalogueStats computation."""

from library_catalogue.models import Book
from library_catalogue.site_generator.stats import compute_stats


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


def test_compute_stats_counts_totals_and_available() -> None:
    books = [
        make_book(id="BK000001", genre="Fantasy", status="Available"),
        make_book(id="BK000002", genre="Science Fiction", status="On Loan"),
        make_book(id="BK000003", genre="Fantasy", status="Reserved"),
    ]
    stats = compute_stats(books)
    assert stats.total_books == 3
    assert stats.available_count == 1


def test_compute_stats_genres_are_sorted_and_unique() -> None:
    books = [
        make_book(id="BK000001", genre="Science Fiction"),
        make_book(id="BK000002", genre="Fantasy"),
        make_book(id="BK000003", genre="Fantasy"),
    ]
    stats = compute_stats(books)
    assert stats.genres == ("Fantasy", "Science Fiction")


def test_compute_stats_languages_are_sorted_and_unique() -> None:
    books = [
        make_book(id="BK000001", language="English"),
        make_book(id="BK000002", language="Tamil"),
        make_book(id="BK000003", language="Tamil"),
        make_book(id="BK000004"),
    ]
    stats = compute_stats(books)
    assert stats.languages == ("English", "Tamil")
