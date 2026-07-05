"""Renders HTML pages from Jinja2 templates."""

from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from library_catalogue.site_generator.stats import CatalogueStats


class PageGenerator:
    """Thin wrapper around a Jinja2 Environment for the two page types."""

    def __init__(self, templates_dir: Path) -> None:
        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render_index_page(self, books: list[dict[str, Any]], stats: CatalogueStats) -> str:
        template = self.env.get_template("index.html")
        return template.render(books=books, stats=stats, asset_base=".")

    def render_book_page(self, book: dict[str, Any]) -> str:
        template = self.env.get_template("book.html")
        return template.render(book=book, asset_base="..")
