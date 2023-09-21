from abc import ABC, abstractmethod
from django.db import IntegrityError
import requests

import requests

from book.models import Book


class BookApi(ABC):
    @abstractmethod
    def search(self, query, page):
        pass


class BookSearchService(BookApi):
    @staticmethod
    def search(query, page):
        results_list = list(Book.objects.filter(title__icontains=query))
        total_results = len(results_list)
        return results_list, total_results

# TODO 多分サービスに入れたほうが良さそう
class GoogleBooksAPIService(BookApi):
    @staticmethod
    def search(query, page):
        startIndex = (int(page) - 1) * 10
        GOOGLE_BOOKS_API_URL = f"https://www.googleapis.com/books/v1/volumes?q={query}&startIndex={startIndex}&maxResults=10&langRestrict=ja&Country=JP"
        response = requests.get(GOOGLE_BOOKS_API_URL)
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            total_items = data.get("totalItems", 0)
            results_list = []
            for item in items:
                volume_info = item.get("volumeInfo", {})
                industry_identifiers = volume_info.get("industryIdentifiers", [])

                isbn_10 = ""
                isbn_13 = ""

                if len(industry_identifiers) > 0:
                    isbn_10 = industry_identifiers[0].get("identifier", "")
                if len(industry_identifiers) > 1:
                    isbn_13 = industry_identifiers[1].get("identifier", "")

                if not isbn_10 or not isbn_13:
                    print("None create")
                    continue
                
                try:
                    book, created = Book.objects.get_or_create(
                        title=volume_info.get("title", "Unknown Title"),
                        description=volume_info.get("description", ""),
                        thumbnail=volume_info.get("imageLinks", {}).get("thumbnail", ""),
                        isbn_10=isbn_10,
                        isbn_13=isbn_13,
                    )
                    results_list.append(book)
                except Exception as e:
                    continue

            return results_list, total_items
        return [], 0
