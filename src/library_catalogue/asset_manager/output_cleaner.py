"""Safely empties the output directory before a build."""

import logging
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)


class UnsafeOutputPathError(Exception):
    """Raised when the configured output path looks too dangerous to clean."""


def clean_output_dir(output_dir: Path) -> None:
    """Remove everything inside ``output_dir`` (creating it if needed).

    Refuses to operate on the filesystem root, a user's home directory, or
    any path that isn't itself named ``output`` -- a cheap guard against a
    misconfigured path wiping out something unintended.
    """
    resolved = output_dir.resolve()

    if resolved == Path(resolved.anchor) or resolved == Path.home():
        raise UnsafeOutputPathError(f"Refusing to clean unsafe output path: {resolved}")
    if resolved.name != "output":
        raise UnsafeOutputPathError(f"Refusing to clean output path not named 'output': {resolved}")

    if resolved.exists():
        shutil.rmtree(resolved)
    resolved.mkdir(parents=True, exist_ok=True)
    logger.info("Cleaned output directory: %s", resolved)
