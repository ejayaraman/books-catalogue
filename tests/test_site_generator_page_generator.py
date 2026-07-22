"""Tests for Jinja2 page rendering."""

from pathlib import Path

from library_catalogue.models import Book
from library_catalogue.site_generator.context_builder import book_to_dict
from library_catalogue.site_generator.page_generator import PageGenerator
from library_catalogue.site_generator.stats import compute_stats

TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "templates"


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


def test_render_book_page_contains_expected_fields() -> None:
    generator = PageGenerator(TEMPLATES_DIR)
    book = make_book(
        isbn="9780441013593", shelf="A1", description="A young duke leads a desert revolt."
    )
    book_dict = book_to_dict(book, cover_url="covers/BK000001.jpg", page_url="books/BK000001.html")

    html = generator.render_book_page(book_dict)

    assert "Dune" in html
    assert "Frank Herbert" in html
    assert "9780441013593" in html
    assert "status-available" in html
    assert 'href="../index.html"' in html
    assert "Shelf" in html and "A1" in html
    assert "A young duke leads a desert revolt." in html


def test_render_book_page_omits_blank_description() -> None:
    generator = PageGenerator(TEMPLATES_DIR)
    book = make_book(description=None)
    book_dict = book_to_dict(
        book, cover_url="covers/placeholder.jpg", page_url="books/BK000001.html"
    )

    html = generator.render_book_page(book_dict)

    assert "book-description" not in html


def test_render_book_page_omits_blank_shelf() -> None:
    generator = PageGenerator(TEMPLATES_DIR)
    book = make_book(shelf=None)
    book_dict = book_to_dict(
        book, cover_url="covers/placeholder.jpg", page_url="books/BK000001.html"
    )

    html = generator.render_book_page(book_dict)

    assert "Shelf" not in html


def test_render_index_page_contains_counts_and_titles() -> None:
    generator = PageGenerator(TEMPLATES_DIR)
    books = [
        make_book(id="BK000001", title="Dune", row_number=1),
        make_book(id="BK000002", title="Foundation", row_number=2),
    ]
    stats = compute_stats(books)
    book_dicts = [
        book_to_dict(book, cover_url="covers/placeholder.jpg", page_url=f"books/{book.id}.html")
        for book in books
    ]

    html = generator.render_index_page(book_dicts, stats)

    assert "Dune" in html
    assert "Foundation" in html
    assert 'id="total-count">2' in html
    assert 'href="books/BK000001.html"' in html


def test_render_credits_page_lists_sources() -> None:
    generator = PageGenerator(TEMPLATES_DIR)

    html = generator.render_credits_page()

    assert "Claude Code" in html
    assert "Google Books" in html
    assert "Open Library" in html
    assert "Goodreads" in html
    assert "Panuval.com" in html
