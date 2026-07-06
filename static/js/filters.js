// Composes genre and language filters with AND logic. "all" bypasses a filter.
export function apply(books, { genre, language }) {
  return books.filter((book) => {
    if (genre && genre !== "all" && book.genre !== genre) {
      return false;
    }
    if (language && language !== "all" && book.language !== language) {
      return false;
    }
    return true;
  });
}
