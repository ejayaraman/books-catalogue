// Entry module for the catalogue page: fetches books.json, wires the search
// box, filters and sort control, and re-renders the existing card grid.
import { matches } from "./search.js";
import { apply as applyFilters } from "./filters.js";
import { sort as sortBooks } from "./sorting.js";
import { paginate, PAGE_SIZE } from "./pagination.js";

const state = { query: "", genre: "all", language: "all", sort: "recent", page: 1 };

function renderPagination(paginationEl, page, totalPages, onChange) {
  paginationEl.innerHTML = "";
  if (totalPages <= 1) {
    return;
  }

  const prevButton = document.createElement("button");
  prevButton.type = "button";
  prevButton.textContent = "Previous";
  prevButton.disabled = page <= 1;
  prevButton.addEventListener("click", () => onChange(page - 1));

  const status = document.createElement("span");
  status.className = "pagination-status";
  status.textContent = `Page ${page} of ${totalPages}`;

  const nextButton = document.createElement("button");
  nextButton.type = "button";
  nextButton.textContent = "Next";
  nextButton.disabled = page >= totalPages;
  nextButton.addEventListener("click", () => onChange(page + 1));

  paginationEl.append(prevButton, status, nextButton);
}

function recompute(books, cardsById, resultsCountEl, paginationEl, grid) {
  const filtered = applyFilters(books, { genre: state.genre, language: state.language });
  const searched = filtered.filter((book) => matches(book, state.query));
  const sorted = sortBooks(searched, state.sort);
  const { items: pageItems, page, totalPages } = paginate(sorted, state.page);
  state.page = page;
  const visibleIds = new Set(pageItems.map((book) => book.id));

  cardsById.forEach((card, id) => {
    card.style.display = visibleIds.has(id) ? "" : "none";
  });

  pageItems.forEach((book) => {
    const card = cardsById.get(book.id);
    if (card) {
      grid.appendChild(card);
    }
  });

  if (sorted.length === 0) {
    resultsCountEl.textContent = "Showing 0 of 0 books";
  } else {
    const start = (page - 1) * PAGE_SIZE + 1;
    const end = start + pageItems.length - 1;
    resultsCountEl.textContent = `Showing ${start}-${end} of ${sorted.length} books`;
  }

  renderPagination(paginationEl, page, totalPages, (newPage) => {
    state.page = newPage;
    recompute(books, cardsById, resultsCountEl, paginationEl, grid);
    grid.scrollIntoView({ behavior: "smooth", block: "start" });
  });
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
  const languageFilter = document.getElementById("language-filter");
  const sortSelect = document.getElementById("sort-select");
  const resultsCountEl = document.getElementById("results-count");
  const paginationEl = document.getElementById("pagination");

  const update = () => recompute(books, cardsById, resultsCountEl, paginationEl, grid);
  const updateFromScratch = () => {
    state.page = 1;
    update();
  };

  searchInput.addEventListener("input", () => {
    state.query = searchInput.value.trim();
    updateFromScratch();
  });
  genreFilter.addEventListener("change", () => {
    state.genre = genreFilter.value;
    updateFromScratch();
  });
  languageFilter.addEventListener("change", () => {
    state.language = languageFilter.value;
    updateFromScratch();
  });
  sortSelect.addEventListener("change", () => {
    state.sort = sortSelect.value;
    updateFromScratch();
  });

  update();
});
