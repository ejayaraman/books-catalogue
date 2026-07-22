"""End-to-end integration test for the full build pipeline."""

import json
from pathlib import Path

import pytest

from library_catalogue.library_reader import read_spreadsheet
from library_catalogue.site_generator import run_build
from library_catalogue.site_generator.pipeline import BuildAbortedError
from tests.conftest import make_build_config


def test_full_build_produces_expected_output(valid_spreadsheet: Path, tmp_path: Path) -> None:
    output_dir = tmp_path / "output"
    config = make_build_config(valid_spreadsheet, output_dir)

    summary = run_build(config)

    books = read_spreadsheet(valid_spreadsheet)
    assert summary.book_count == len(books)
    assert summary.error_count == 0

    assert (output_dir / "index.html").exists()
    assert (output_dir / "credits.html").exists()
    assert (output_dir / "books.json").exists()

    for book in books:
        assert (output_dir / "books" / f"{book.id}.html").exists()

    assert (output_dir / "static" / "css" / "base.css").exists()
    assert (output_dir / "covers" / "placeholder.jpg").exists()

    catalogue = json.loads((output_dir / "books.json").read_text())
    assert len(catalogue) == len(books)


def test_full_build_aborts_on_invalid_spreadsheet(
    invalid_spreadsheet: Path, tmp_path: Path
) -> None:
    output_dir = tmp_path / "output"
    config = make_build_config(invalid_spreadsheet, output_dir)

    with pytest.raises(BuildAbortedError):
        run_build(config)

    assert not output_dir.exists() or list(output_dir.iterdir()) == []
