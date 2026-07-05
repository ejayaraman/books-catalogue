"""Generates books.json and the static HTML site from validated Book data."""

from library_catalogue.site_generator.context_builder import book_to_dict
from library_catalogue.site_generator.json_writer import build_catalogue_json, write_json
from library_catalogue.site_generator.page_generator import PageGenerator
from library_catalogue.site_generator.pipeline import BuildAbortedError, run_build
from library_catalogue.site_generator.stats import CatalogueStats, compute_stats

__all__ = [
    "book_to_dict",
    "build_catalogue_json",
    "write_json",
    "PageGenerator",
    "BuildAbortedError",
    "run_build",
    "CatalogueStats",
    "compute_stats",
]
