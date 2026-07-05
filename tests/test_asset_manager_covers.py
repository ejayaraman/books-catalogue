"""Tests for cover resolution and copying."""

from pathlib import Path

import pytest

from library_catalogue.asset_manager.covers import copy_covers, resolve_cover_path
from library_catalogue.models import Book


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


@pytest.fixture
def placeholder_cover(tmp_path: Path) -> Path:
    path = tmp_path / "placeholder.jpg"
    path.write_bytes(b"placeholder-bytes")
    return path


def test_resolve_cover_path_finds_matching_id(tmp_path: Path) -> None:
    (tmp_path / "BK000001.jpg").write_bytes(b"cover-bytes")
    result = resolve_cover_path(make_book(id="BK000001"), tmp_path)
    assert result == tmp_path / "BK000001.jpg"


def test_resolve_cover_path_honors_explicit_override(tmp_path: Path) -> None:
    (tmp_path / "custom-name.png").write_bytes(b"cover-bytes")
    book = make_book(cover_image="custom-name.png")
    assert resolve_cover_path(book, tmp_path) == tmp_path / "custom-name.png"


def test_resolve_cover_path_returns_none_when_absent(tmp_path: Path) -> None:
    assert resolve_cover_path(make_book(id="BK999999"), tmp_path) is None


def test_copy_covers_copies_existing_and_placeholder(
    tmp_path: Path, placeholder_cover: Path
) -> None:
    covers_dir = tmp_path / "covers"
    covers_dir.mkdir()
    (covers_dir / "BK000001.jpg").write_bytes(b"cover-bytes")

    output_dir = tmp_path / "output"
    books = [make_book(id="BK000001"), make_book(id="BK000002")]

    result = copy_covers(books, covers_dir, output_dir, placeholder_cover)

    assert (output_dir / "covers" / "BK000001.jpg").exists()
    assert (output_dir / "covers" / "placeholder.jpg").exists()
    assert result.cover_url_by_book_id["BK000001"] == "covers/BK000001.jpg"
    assert result.cover_url_by_book_id["BK000002"] == "covers/placeholder.jpg"
