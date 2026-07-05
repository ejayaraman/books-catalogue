"""Tests for building and writing books.json."""

import json
from pathlib import Path

from library_catalogue.models import Book
from library_catalogue.site_generator.json_writer import build_catalogue_json, write_json


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


def test_build_catalogue_json_preserves_order_and_shape() -> None:
    books = [
        make_book(id="BK000001", row_number=1),
        make_book(id="BK000002", row_number=2, shelf=None),
    ]
    data = build_catalogue_json(books, cover_url_by_book_id={"BK000001": "covers/BK000001.jpg"})

    assert [entry["id"] for entry in data] == ["BK000001", "BK000002"]
    assert data[0]["cover_url"] == "covers/BK000001.jpg"
    assert data[1]["cover_url"] == "covers/placeholder.jpg"
    assert data[1]["shelf"] is None
    assert data[0]["page_url"] == "books/BK000001.html"
    assert data[0]["order"] == 0


def test_write_json_is_byte_identical_across_runs(tmp_path: Path) -> None:
    data = [{"id": "BK000001", "title": "Dune"}]
    path_a = tmp_path / "a.json"
    path_b = tmp_path / "b.json"
    write_json(data, path_a)
    write_json(data, path_b)
    assert path_a.read_bytes() == path_b.read_bytes()


def test_write_json_is_valid_json(tmp_path: Path) -> None:
    data = [{"id": "BK000001", "title": "Dune"}]
    path = tmp_path / "books.json"
    write_json(data, path)
    assert json.loads(path.read_text()) == data
