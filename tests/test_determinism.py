"""Confirms that rebuilding without changing the spreadsheet is byte-identical."""

from pathlib import Path

from library_catalogue.site_generator import run_build
from tests.conftest import make_build_config


def test_two_builds_produce_byte_identical_output(valid_spreadsheet: Path, tmp_path: Path) -> None:
    output_a = tmp_path / "run_a" / "output"
    output_b = tmp_path / "run_b" / "output"

    run_build(make_build_config(valid_spreadsheet, output_a))
    run_build(make_build_config(valid_spreadsheet, output_b))

    files_a = sorted(path.relative_to(output_a) for path in output_a.rglob("*") if path.is_file())
    files_b = sorted(path.relative_to(output_b) for path in output_b.rglob("*") if path.is_file())
    assert files_a == files_b

    for relative_path in files_a:
        assert (output_a / relative_path).read_bytes() == (
            output_b / relative_path
        ).read_bytes(), f"{relative_path} differs between runs"
