from abc import ABC, abstractmethod

from book.domain.repositories import BookRepository
from book.domain.services import BookDomainService
from book.infrastructure.mappers import GoogleBooksMapper


# 検索ドメイン
class SearchDomainService(ABC):
    @abstractmethod
    def search(self, query, page):
        pass


class BookSearchService(SearchDomainService):
    """書籍検索。"""

    def __init__(self):
        self.repository = BookRepository()

    def search(self, query, page):
        results_list = self.repository.search_by_title(query)
        total_results = len(results_list)
        total_pages = (total_results // 10) + (1 if total_results % 10 else 1)
        return results_list[(page - 1) * 10 : page * 10], total_pages


class GoogleBooksService(SearchDomainService):
    """Google Books APIを利用した書籍検索。"""

    def __init__(self, api_client, book_service: BookDomainService):
        self.api_client = api_client
        self.book_service = book_service

    def search(self, query, page):
        api_result = self.api_client.fetch_books(query, page)
        book_items = api_result.get("items", [])

        books_data = GoogleBooksMapper.to_books(book_items)

        print(str(len(books_data)) + "件の書籍を登録します")

        books = self.book_service.get_or_create_books(books_data)

        total_items = api_result.get("totalItems", 0)
        total_pages = (total_items // 10) + (1 if total_items % 10 else 0)

        return books, total_pages
