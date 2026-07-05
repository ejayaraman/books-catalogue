// Sorts books by the four supported keys without mutating the input array.
export function sort(books, key) {
  const copy = books.slice();
  switch (key) {
    case "title":
      copy.sort((a, b) => a.title.localeCompare(b.title));
      break;
    case "author":
      copy.sort((a, b) => a.author.localeCompare(b.author));
      break;
    case "year":
      copy.sort((a, b) => (b.publication_year || 0) - (a.publication_year || 0));
      break;
    case "recent":
    default:
      copy.sort((a, b) => b.order - a.order);
      break;
  }
  return copy;
}
