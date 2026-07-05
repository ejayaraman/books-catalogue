"""Tests for static asset copying."""

from pathlib import Path

from library_catalogue.asset_manager.static_assets import copy_static_assets


def test_copy_static_assets_preserves_subfolders(tmp_path: Path) -> None:
    static_dir = tmp_path / "static"
    (static_dir / "css").mkdir(parents=True)
    (static_dir / "js").mkdir()
    (static_dir / "images").mkdir()
    (static_dir / "icons").mkdir()
    (static_dir / "css" / "base.css").write_text("body { margin: 0; }")
    (static_dir / "js" / "app.js").write_text("console.log('hi');")

    output_dir = tmp_path / "output"
    result = copy_static_assets(static_dir, output_dir)

    assert (output_dir / "static" / "css" / "base.css").exists()
    assert (output_dir / "static" / "js" / "app.js").exists()
    assert (output_dir / "static" / "images").is_dir()
    assert (output_dir / "static" / "icons").is_dir()
    assert len(result) == 2
