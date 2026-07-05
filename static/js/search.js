// Matches a book against a free-text search query.
export function matches(book, query) {
  if (!query) {
    return true;
  }
  const haystack = [
    book.title,
    book.author,
    book.isbn,
    book.genre,
    book.publisher,
    (book.tags || []).join(" "),
  ]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();
  return haystack.includes(query.toLowerCase());
}
