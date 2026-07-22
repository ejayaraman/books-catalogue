"""Orchestrates the 8-step build process described in the requirements."""

import logging
import time
from pathlib import Path
from typing import Any

from library_catalogue.asset_manager import clean_output_dir, copy_covers, copy_static_assets
from library_catalogue.asset_manager.covers import PLACEHOLDER_NAME
from library_catalogue.library_reader import read_spreadsheet
from library_catalogue.models import Book, BuildConfig, BuildSummary, ValidationReport
from library_catalogue.site_generator.context_builder import book_to_dict
from library_catalogue.site_generator.json_writer import build_catalogue_json, write_json
from library_catalogue.site_generator.page_generator import PageGenerator
from library_catalogue.site_generator.stats import CatalogueStats, compute_stats
from library_catalogue.validators import validate

logger = logging.getLogger(__name__)


class BuildAbortedError(Exception):
    """Raised when validation finds hard errors; the report is attached."""

    def __init__(self, report: ValidationReport) -> None:
        super().__init__("Build aborted: validation found blocking errors")
        self.report = report


def generate_book_pages(
    books: list[Book],
    cover_url_by_book_id: dict[str, str],
    generator: PageGenerator,
    output_dir: Path,
) -> int:
    """Render one HTML page per book into output/books/."""
    books_dir = output_dir / "books"
    books_dir.mkdir(parents=True, exist_ok=True)
    for book in books:
        cover_url = cover_url_by_book_id.get(book.id, f"covers/{PLACEHOLDER_NAME}")
        book_dict = book_to_dict(book, cover_url=cover_url, page_url=f"books/{book.id}.html")
        html = generator.render_book_page(book_dict)
        (books_dir / f"{book.id}.html").write_text(html, encoding="utf-8")
    logger.info("Generated %d book page(s)", len(books))
    return len(books)


def generate_index_page(
    book_dicts: list[dict[str, Any]],
    stats: CatalogueStats,
    generator: PageGenerator,
    output_dir: Path,
) -> None:
    """Render the catalogue index page into output/index.html."""
    html = generator.render_index_page(book_dicts, stats)
    (output_dir / "index.html").write_text(html, encoding="utf-8")
    logger.info("Generated index page")


def generate_credits_page(generator: PageGenerator, output_dir: Path) -> None:
    """Render the static credits page into output/credits.html."""
    html = generator.render_credits_page()
    (output_dir / "credits.html").write_text(html, encoding="utf-8")
    logger.info("Generated credits page")


def run_build(config: BuildConfig) -> BuildSummary:
    """Run the full 8-step build pipeline and return a summary."""
    start = time.perf_counter()

    books = read_spreadsheet(config.spreadsheet_path)  # 1. read

    report = validate(books, config.covers_dir)  # 2. validate
    for line in report.summary_lines(len(books)):
        logger.info(line)
    if report.has_errors:
        raise BuildAbortedError(report)

    clean_output_dir(config.output_dir)  # 3. clean output

    static_result = copy_static_assets(config.static_dir, config.output_dir)  # 4. copy assets
    covers_result = copy_covers(
        books, config.covers_dir, config.output_dir, config.placeholder_cover_path
    )
    assets_result = static_result + covers_result

    json_data = build_catalogue_json(books, covers_result.cover_url_by_book_id)  # 5. generate JSON
    write_json(json_data, config.output_dir / "books.json")

    generator = PageGenerator(config.templates_dir)
    pages_generated = generate_book_pages(  # 6. individual book pages
        books, covers_result.cover_url_by_book_id, generator, config.output_dir
    )

    stats = compute_stats(books)
    generate_index_page(json_data, stats, generator, config.output_dir)  # 7. catalogue page
    pages_generated += 1

    generate_credits_page(generator, config.output_dir)  # credits page
    pages_generated += 1

    duration = time.perf_counter() - start
    summary = BuildSummary(  # 8. build summary
        book_count=len(books),
        error_count=len(report.errors),
        warning_count=len(report.warnings),
        pages_generated=pages_generated,
        assets_copied=len(assets_result),
        duration_seconds=duration,
    )
    logger.info(summary.format())
    return summary
