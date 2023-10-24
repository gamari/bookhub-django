import logging

logger = logging.getLogger("app_logger")

class GoogleBooksMapper(object):
    @staticmethod
    def to_books(items):
        """ISBNがない場合は何も返さない"""
        books = []

        for item in items:
            volume_info = item.get("volumeInfo", {})

            # ISBN処理
            industry_identifiers = volume_info.get("industryIdentifiers", [])

            isbn_10 = None
            isbn_13 = None
            other = None

            for identifier in industry_identifiers:
                if identifier.get("type") == "ISBN_10":
                    isbn_10 = identifier.get("identifier")
                elif identifier.get("type") == "ISBN_13":
                    isbn_13 = identifier.get("identifier")
                elif identifier.get("type") == "OTHER":
                    other = identifier.get("identifier")

            if not isbn_10 and not isbn_13 and not other:
                logger.info("no isbn" + volume_info.get("title") + str(industry_identifiers))
                continue

            authors = volume_info.get("authors", [])

            title = volume_info.get("title", "")
            description = volume_info.get("description", "")
            thumbnail = volume_info.get("imageLinks", {}).get("thumbnail", "")
            published_date = volume_info.get("publishedDate", "")
            publisher = volume_info.get("publisher", "")

            book = {
                "title": title,
                "description": description,
                "thumbnail": thumbnail,
                "isbn_10": isbn_10,
                "isbn_13": isbn_13,
                "other": other,
                "authors": authors,
                "published_date": published_date,
                "publisher": publisher,
            }
            books.append(book)

        return books
