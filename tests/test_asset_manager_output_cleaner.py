"""Tests for the output directory cleaner and its safety guard."""

from pathlib import Path

import pytest

from library_catalogue.asset_manager.output_cleaner import (
    UnsafeOutputPathError,
    clean_output_dir,
)


def test_clean_output_dir_empties_populated_directory(tmp_path: Path) -> None:
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    (output_dir / "stale.html").write_text("old")
    (output_dir / "books").mkdir()
    (output_dir / "books" / "BK000001.html").write_text("old")

    clean_output_dir(output_dir)

    assert output_dir.exists()
    assert list(output_dir.iterdir()) == []


def test_clean_output_dir_creates_missing_directory(tmp_path: Path) -> None:
    output_dir = tmp_path / "output"
    clean_output_dir(output_dir)
    assert output_dir.exists()


def test_clean_output_dir_rejects_path_not_named_output(tmp_path: Path) -> None:
    unsafe_dir = tmp_path / "not-output"
    unsafe_dir.mkdir()
    with pytest.raises(UnsafeOutputPathError):
        clean_output_dir(unsafe_dir)


def test_clean_output_dir_rejects_home_directory() -> None:
    with pytest.raises(UnsafeOutputPathError):
        clean_output_dir(Path.home())
