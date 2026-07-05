"""Copies the static/ directory (css/js/images/icons) into the output directory."""

import logging
import shutil
from pathlib import Path

from library_catalogue.asset_manager.covers import AssetCopyResult

logger = logging.getLogger(__name__)


def copy_static_assets(static_dir: Path, output_dir: Path) -> AssetCopyResult:
    """Copy the entire static/ tree into output/static/, preserving subfolders."""
    dest = output_dir / "static"
    shutil.copytree(static_dir, dest, dirs_exist_ok=True)
    copied_paths = sorted(path for path in dest.rglob("*") if path.is_file())
    logger.info("Copied %d static asset(s) to %s", len(copied_paths), dest)
    return AssetCopyResult(copied_paths=copied_paths)
