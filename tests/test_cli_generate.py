"""Tests for the generate.py CLI entry point."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import generate  # noqa: E402


def test_main_exits_zero_and_builds_site(valid_spreadsheet: Path, tmp_path: Path) -> None:
    output_dir = tmp_path / "output"
    exit_code = generate.main(["--data", str(valid_spreadsheet), "--output", str(output_dir)])
    assert exit_code == 0
    assert (output_dir / "index.html").exists()
    assert (output_dir / "books.json").exists()


def test_main_exits_one_and_writes_nothing_on_invalid_spreadsheet(
    invalid_spreadsheet: Path, tmp_path: Path
) -> None:
    output_dir = tmp_path / "output"
    exit_code = generate.main(["--data", str(invalid_spreadsheet), "--output", str(output_dir)])
    assert exit_code == 1
    assert not output_dir.exists() or list(output_dir.iterdir()) == []


def test_main_exits_one_on_missing_spreadsheet(tmp_path: Path) -> None:
    exit_code = generate.main(
        ["--data", str(tmp_path / "does_not_exist.csv"), "--output", str(tmp_path / "output")]
    )
    assert exit_code == 1
