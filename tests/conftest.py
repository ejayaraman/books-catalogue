"""Shared pytest fixtures."""

from pathlib import Path

import pytest

from library_catalogue.models import BuildConfig

FIXTURES_DIR = Path(__file__).parent / "fixtures"
PROJECT_ROOT = Path(__file__).parent.parent


@pytest.fixture
def valid_spreadsheet() -> Path:
    return FIXTURES_DIR / "valid_books.csv"


@pytest.fixture
def invalid_spreadsheet() -> Path:
    return FIXTURES_DIR / "invalid_books.csv"


@pytest.fixture
def fixture_covers_dir() -> Path:
    return FIXTURES_DIR / "covers"


def make_build_config(spreadsheet_path: Path, output_dir: Path) -> BuildConfig:
    """Build config using real templates/static assets but fixture data and a tmp output dir."""
    return BuildConfig(
        spreadsheet_path=spreadsheet_path,
        templates_dir=PROJECT_ROOT / "templates",
        static_dir=PROJECT_ROOT / "static",
        covers_dir=FIXTURES_DIR / "covers",
        output_dir=output_dir,
        placeholder_cover_path=PROJECT_ROOT / "static" / "images" / "placeholder-cover.jpg",
    )
