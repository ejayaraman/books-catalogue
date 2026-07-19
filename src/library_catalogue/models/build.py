"""Build configuration and summary types for the generation pipeline."""

from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]


@dataclass(frozen=True)
class BuildConfig:
    """Every path the pipeline needs, resolved up front.

    Constructed via :meth:`default` for real runs, or directly in tests so
    every path can point at a ``tmp_path`` fixture without touching the real
    project tree.
    """

    spreadsheet_path: Path
    templates_dir: Path
    static_dir: Path
    covers_dir: Path
    output_dir: Path
    placeholder_cover_path: Path

    @classmethod
    def default(cls, project_root: Path | None = None) -> "BuildConfig":
        root = project_root or PROJECT_ROOT
        return cls(
            spreadsheet_path=root / "data" / "books.csv",
            templates_dir=root / "templates",
            static_dir=root / "static",
            covers_dir=root / "covers",
            output_dir=root / "output",
            placeholder_cover_path=root / "static" / "images" / "placeholder-cover.jpg",
        )


@dataclass(frozen=True)
class BuildSummary:
    book_count: int
    error_count: int
    warning_count: int
    pages_generated: int
    assets_copied: int
    duration_seconds: float

    def format(self) -> str:
        return (
            f"Build complete: {self.book_count} books, {self.pages_generated} pages, "
            f"{self.assets_copied} assets copied, {self.warning_count} warnings "
            f"in {self.duration_seconds:.2f}s"
        )
