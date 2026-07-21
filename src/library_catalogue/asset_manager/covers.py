"""Resolves and copies book cover images.

``resolve_cover_path`` is the single source of truth for "does this book have
a cover image" -- it is called both by the validator's missing-cover warning
and by the actual copy step, so the two can never disagree.
"""

import logging
import shutil
from dataclasses import dataclass, field
from pathlib import Path

from library_catalogue.models import Book

try:
    from PIL import Image

    _PILLOW_AVAILABLE = True
except ImportError:
    _PILLOW_AVAILABLE = False

logger = logging.getLogger(__name__)

COVER_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")

PLACEHOLDER_NAME = "placeholder.jpg"

MAX_COVER_HEIGHT = 1000
JPEG_QUALITY = 80


def resolve_cover_path(book: Book, covers_dir: Path) -> Path | None:
    """Find the cover image file for a book, or None if it has none.

    Honors an explicit ``Cover Image`` override first; otherwise looks for
    ``<ID>.jpg`` / ``.jpeg`` / ``.png`` / ``.webp`` in that order.
    """
    if book.cover_image:
        candidate = covers_dir / book.cover_image
        return candidate if candidate.is_file() else None

    for extension in COVER_EXTENSIONS:
        candidate = covers_dir / f"{book.id}{extension}"
        if candidate.is_file():
            return candidate
    return None


def _copy_cover(source: Path, dest: Path) -> None:
    """Copy a cover image, downscaling it if Pillow is available.

    Falls back to a plain byte copy when Pillow isn't installed, or when the
    source can't be decoded as an image (e.g. an unsupported format).
    """
    if not _PILLOW_AVAILABLE:
        shutil.copy2(source, dest)
        return

    try:
        with Image.open(source) as image:
            if image.height > MAX_COVER_HEIGHT:
                ratio = MAX_COVER_HEIGHT / image.height
                new_size = (round(image.width * ratio), MAX_COVER_HEIGHT)
                image = image.resize(new_size, Image.LANCZOS)

            suffix = dest.suffix.lower()
            if suffix in (".jpg", ".jpeg"):
                if image.mode != "RGB":
                    image = image.convert("RGB")
                image.save(dest, quality=JPEG_QUALITY, optimize=True)
            elif suffix == ".webp":
                image.save(dest, quality=JPEG_QUALITY)
            else:
                image.save(dest, optimize=True)

        # Resampling can occasionally bloat file size (e.g. a flat-color PNG
        # with transparency) even though the pixel dimensions shrank. Never
        # ship a "resized" cover that's bigger than the original.
        if dest.stat().st_size > source.stat().st_size:
            shutil.copy2(source, dest)
    except Exception:
        logger.warning("Could not resize cover %s, copying as-is", source, exc_info=True)
        shutil.copy2(source, dest)


@dataclass
class AssetCopyResult:
    copied_paths: list[Path] = field(default_factory=list)
    cover_url_by_book_id: dict[str, str] = field(default_factory=dict)

    def __len__(self) -> int:
        return len(self.copied_paths)

    def __add__(self, other: "AssetCopyResult") -> "AssetCopyResult":
        return AssetCopyResult(
            copied_paths=self.copied_paths + other.copied_paths,
            cover_url_by_book_id={**self.cover_url_by_book_id, **other.cover_url_by_book_id},
        )


def copy_covers(
    books: list[Book],
    covers_dir: Path,
    output_dir: Path,
    placeholder_cover_path: Path,
) -> AssetCopyResult:
    """Copy each book's cover (or the shared placeholder) into ``output_dir/covers``."""
    output_covers_dir = output_dir / "covers"
    output_covers_dir.mkdir(parents=True, exist_ok=True)

    placeholder_dest = output_covers_dir / PLACEHOLDER_NAME
    shutil.copy2(placeholder_cover_path, placeholder_dest)
    result = AssetCopyResult(copied_paths=[placeholder_dest])

    for book in sorted(books, key=lambda b: b.id):
        source = resolve_cover_path(book, covers_dir)
        if source is None:
            result.cover_url_by_book_id[book.id] = f"covers/{PLACEHOLDER_NAME}"
            continue
        dest = output_covers_dir / f"{book.id}{source.suffix.lower()}"
        _copy_cover(source, dest)
        result.copied_paths.append(dest)
        result.cover_url_by_book_id[book.id] = f"covers/{dest.name}"

    return result
