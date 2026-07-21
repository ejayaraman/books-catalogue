"""Builds the per-book dict shared by books.json and the Jinja templates."""

from typing import Any

from library_catalogue.models import Book, status_slug


def book_to_dict(book: Book, cover_url: str, page_url: str) -> dict[str, Any]:
    """Convert a Book into the dict shape used by books.json and templates.

    This is the single place a Book's fields become plain data, so the
    catalogue JSON, the index page cards, and the book detail page all stay
    in sync with each other.
    """
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "isbn": book.isbn,
        "genre": book.genre,
        "language": book.language,
        "publisher": book.publisher,
        "publication_year": book.publication_year,
        "shelf": book.shelf,
        "status": book.status,
        "status_slug": status_slug(book.status),
        "tags": list(book.tags),
        "notes": book.notes,
        "rating": book.rating,
        "description": book.description,
        "cover_url": cover_url,
        "page_url": page_url,
        "order": book.row_number - 1,
    }
