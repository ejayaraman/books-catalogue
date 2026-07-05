// Dark mode toggle. Runs on every page (loaded from base.html).
const STORAGE_KEY = "catalogue-theme";

function applyTheme(theme) {
  document.documentElement.setAttribute("data-theme", theme);
}

function currentTheme() {
  return document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light";
}

function toggleTheme() {
  const next = currentTheme() === "dark" ? "light" : "dark";
  applyTheme(next);
  localStorage.setItem(STORAGE_KEY, next);
}

document.addEventListener("DOMContentLoaded", () => {
  const button = document.getElementById("theme-toggle");
  if (button) {
    button.addEventListener("click", toggleTheme);
  }
});
