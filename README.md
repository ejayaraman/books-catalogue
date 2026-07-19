# Personal Library Catalogue Generator

Generates a fully static website for a personal collection of physical books from
a CSV file. No database, no backend, no web server required to view it —
just open `output/index.html`, or serve the `output/` folder however you like
(including GitHub Pages, unmodified).

## Requirements

- Python 3.12+

## Installation

```bash
python3.12 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev,images]"
```

`images` (Pillow) is optional — without it, cover thumbnails simply fall back to
the full-size cover image.

## Usage

1. Fill in `data/books.csv` with your collection (see **CSV format** below).
2. Put cover images in `covers/`, named `<ID>.jpg` (or `.jpeg`/`.png`/`.webp`), e.g.
   `covers/BK000001.jpg`. Books without a cover automatically get a placeholder.
3. Run the generator:

   ```bash
   python generate.py
   ```

4. Open `output/index.html` directly in a browser, or serve it locally:

   ```bash
   cd output && python -m http.server
   ```

   Then visit `http://localhost:8000`.

Running `python generate.py` again fully rebuilds `output/` from scratch — it is
safe to re-run at any time and produces deterministic output for the same input.

### CLI options

```bash
python generate.py --data path/to/books.csv --output path/to/output --verbose
```

## CSV format

One row per physical copy. Columns:

| Column           | Required | Notes                                      |
|------------------|----------|---------------------------------------------|
| ID               | Yes      | Unique, e.g. `BK000001`                    |
| Title            | Yes      |                                              |
| Author           | Yes      |                                              |
| ISBN             | No       |                                              |
| Genre            | Yes      |                                              |
| Language         | No       |                                              |
| Publisher        | No       |                                              |
| Publication Year | No       |                                              |
| Shelf            | No       | Omitted from the book page if blank        |
| Status           | Yes      | `Available`, `On Loan`, or `Reserved`      |
| Tags             | No       | Comma-separated                             |
| Notes            | No       |                                              |
| Rating           | No       | Free text, e.g. `4/5`                      |
| Cover Image      | No       | Overrides the `<ID>.<ext>` lookup in `covers/` |

## Validation

Before generating anything, the CSV file is validated. Generation **stops**
if there are duplicate IDs, missing required fields, or invalid status values.
Duplicate ISBNs and missing cover images are reported as warnings only and do
not block the build. A validation summary is always printed first.

## Project structure

```
generate.py             Thin CLI entry point
src/library_catalogue/  Python package (reader, validators, asset manager, site generator)
templates/               Jinja2 templates (base.html, index.html, book.html)
static/                  CSS, JS, images, icons — copied into output/ as-is
data/books.csv           Your CSV file
covers/                  Your cover images
tests/                   pytest suite
output/                  Generated site (safe to delete; regenerated every run)
```

## Development

```bash
pytest                # run tests with coverage
ruff check .          # lint
black .               # format
mypy src              # type-check
```

## Future enhancements (not in this version)

GitHub Pages deployment workflow, borrow-request workflow, QR codes, author pages,
reading statistics, multiple collections, ISBN metadata lookup, import/export tools.
