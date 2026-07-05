"""Tests for the Book dataclass and Status helpers."""

from library_catalogue.models import Book, Status, status_slug


def test_book_required_fields_and_defaults() -> None:
    book = Book(
        id="BK000001",
        title="Dune",
        author="Frank Herbert",
        genre="Science Fiction",
        status="Available",
        row_number=1,
    )
    assert book.id == "BK000001"
    assert book.isbn is None
    assert book.series is None
    assert book.series_number is None
    assert book.publisher is None
    assert book.publication_year is None
    assert book.shelf is None
    assert book.tags == ()
    assert book.notes is None
    assert book.rating is None
    assert book.cover_image is None


def test_book_optional_fields_populated() -> None:
    book = Book(
        id="BK000002",
        title="The Left Hand of Darkness",
        author="Ursula K. Le Guin",
        genre="Science Fiction",
        status="On Loan",
        row_number=2,
        isbn="9780441478125",
        series="Hainish Cycle",
        series_number=4,
        publisher="Ace Books",
        publication_year=1969,
        shelf="A3",
        tags=("favorites", "award-winner"),
        notes="Signed first edition.",
        rating="4/5",
        cover_image="custom-cover.jpg",
    )
    assert book.tags == ("favorites", "award-winner")
    assert book.rating == "4/5"


def test_book_is_frozen() -> None:
    book = Book(
        id="BK000001",
        title="Dune",
        author="Frank Herbert",
        genre="Science Fiction",
        status="Available",
        row_number=1,
    )
    try:
        book.title = "Changed"  # type: ignore[misc]
        raise AssertionError("Book should be immutable")
    except AttributeError:
        pass


def test_status_values() -> None:
    assert Status.values() == {"Available", "On Loan", "Reserved"}


def test_status_slug() -> None:
    assert status_slug("On Loan") == "on-loan"
    assert status_slug("Available") == "available"
    assert Status.ON_LOAN.slug() == "on-loan"
