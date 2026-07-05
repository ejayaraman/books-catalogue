// Entry module for the catalogue page: fetches books.json, wires the search
// box, filters and sort control, and re-renders the existing card grid.
import { matches } from "./search.js";
import { apply as applyFilters } from "./filters.js";
import { sort as sortBooks } from "./sorting.js";

const state = { query: "", genre: "all", status: "all", sort: "recent" };

function recompute(books, cardsById, resultsCountEl, grid) {
  const filtered = applyFilters(books, { genre: state.genre, status: state.status });
  const searched = filtered.filter((book) => matches(book, state.query));
  const sorted = sortBooks(searched, state.sort);
  const visibleIds = new Set(sorted.map((book) => book.id));

  cardsById.forEach((card, id) => {
    card.style.display = visibleIds.has(id) ? "" : "none";
  });

  sorted.forEach((book) => {
    const card = cardsById.get(book.id);
    if (card) {
      grid.appendChild(card);
    }
  });

  resultsCountEl.textContent = `Showing ${sorted.length} of ${books.length} books`;
}

document.addEventListener("DOMContentLoaded", async () => {
  const grid = document.getElementById("book-grid");
  if (!grid) {
    return;
  }

  const response = await fetch("books.json");
  const books = await response.json();

  const cardsById = new Map();
  grid.querySelectorAll(".book-card").forEach((card) => {
    cardsById.set(card.dataset.id, card);
  });

  const searchInput = document.getElementById("search-input");
  const genreFilter = document.getElementById("genre-filter");
  const statusFilter = document.getElementById("status-filter");
  const sortSelect = document.getElementById("sort-select");
  const resultsCountEl = document.getElementById("results-count");

  const update = () => recompute(books, cardsById, resultsCountEl, grid);

  searchInput.addEventListener("input", () => {
    state.query = searchInput.value.trim();
    update();
  });
  genreFilter.addEventListener("change", () => {
    state.genre = genreFilter.value;
    update();
  });
  statusFilter.addEventListener("change", () => {
    state.status = statusFilter.value;
    update();
  });
  sortSelect.addEventListener("change", () => {
    state.sort = sortSelect.value;
    update();
  });

  update();
});
