"""Copies static assets and cover images into the output directory."""

from library_catalogue.asset_manager.covers import (
    AssetCopyResult,
    copy_covers,
    resolve_cover_path,
)
from library_catalogue.asset_manager.output_cleaner import UnsafeOutputPathError, clean_output_dir
from library_catalogue.asset_manager.static_assets import copy_static_assets

__all__ = [
    "AssetCopyResult",
    "copy_covers",
    "resolve_cover_path",
    "clean_output_dir",
    "UnsafeOutputPathError",
    "copy_static_assets",
]
