import logging
from abc import ABC, abstractmethod

from apps.book.domain.repositories import BookRepository
from apps.book.domain.services import BookDomainService
from apps.book.infrastructure.mappers import GoogleBooksMapper
from apps.search.infrastracture.external.apis import GoogleBooksAPIClient

logger = logging.getLogger("app_logger")


# 検索ドメイン
class SearchDomainService(ABC):
    @abstractmethod
    def search(self, query, page, limit=10):
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

    def __init__(self, api_client:GoogleBooksAPIClient, book_service: BookDomainService):
        self.api_client = api_client
        self.book_service = book_service

    def search(self, query, page, limit=10):
        api_result = self.api_client.fetch_books(query, page)
        book_items = api_result.get("items", [])

        logger.debug(str(len(book_items)) + "件を検証します。")
        books_data = GoogleBooksMapper.to_books(book_items)
        logger.debug(str(len(books_data)) + "件の書籍を登録します。")

        # TODO isbn otherどちらもない場合は登録したくない
        books = self.book_service.get_or_create_books(books_data)

        total_items = api_result.get("totalItems", 0)
        total_pages = (total_items // limit) + (1 if total_items % limit else 0)

        return books, total_pages
