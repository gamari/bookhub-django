# mappers.py
class GoogleBooksMapper:
    @staticmethod
    def to_books(items):
        books = []

        for item in items:
            volume_info = item.get("volumeInfo", {})
            industry_identifiers = volume_info.get("industryIdentifiers", [])

            isbn_10 = None
            isbn_13 = None

            for identifier in industry_identifiers:
                if identifier.get("type") == "ISBN_10":
                    isbn_10 = identifier.get("identifier")
                elif identifier.get("type") == "ISBN_13":
                    isbn_13 = identifier.get("identifier")

            if not isbn_10 or not isbn_13:
                continue

            book = {
                "title": volume_info.get("title", "Unknown Title"),
                "description": volume_info.get("description", ""),
                "thumbnail": volume_info.get("imageLinks", {}).get("thumbnail", ""),
                "isbn_10": isbn_10,
                "isbn_13": isbn_13,
            }
            books.append(book)

        return books
