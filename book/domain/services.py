from abc import ABC, abstractmethod
from collections import defaultdict
import datetime
from typing import Any

from book.domain.repositories import BookRepository
from record.domain.repositories import ReadingMemoRepository
from book.infrastructure.external.apis import GoogleBooksAPIClient
from book.infrastructure.mappers import GoogleBooksMapper


# 書籍ドメイン
class BookService:
    def __init__(self, book_repository, review_repository, bookshelf_repository):
        self.book_repository = book_repository
        self.review_repository = review_repository
        self.bookshelf_repository = bookshelf_repository

    def get_book_detail(self, book_id, user):
        book = self.book_repository.find_by_id(book_id)

        if user.is_authenticated:
            latest_review = self.review_repository.latest_review_for_user(book, user)
            book_on_shelf = self.bookshelf_repository.has_book_for_user(book, user)
        else:
            latest_review = None
            book_on_shelf = False
            
        return book, latest_review, book_on_shelf


# 検索ドメイン
class SearchService(ABC):
    @abstractmethod
    def search(self, query, page):
        pass


class BookSearchService(SearchService):
    def __init__(self):
        self.repository = BookRepository()

    def search(self, query, page):
        results_list = self.repository.search_by_title(query)
        total_results = len(results_list)
        total_pages = (total_results // 10) + (1 if total_results % 10 else 1)
        return results_list[(page - 1) * 10 : page * 10], total_pages


class GoogleBooksService(SearchService):
    def __init__(self):
        self.api_client = GoogleBooksAPIClient()
        self.repository = BookRepository()

    def search(self, query, page):
        api_result = self.api_client.fetch_books(query, page)
        book_items = api_result.get("items", [])

        books_data = GoogleBooksMapper.to_books(book_items)

        books = []
        for book_data in books_data:
            book = self.repository.get_or_create(book_data)
            if book:
                books.append(book)

        total_items = api_result.get("totalItems", 0)
        total_pages = (total_items // 10) + (1 if total_items % 10 else 1)

        return books, total_pages


# 活動履歴ドメイン


class ActivityService:
    def fetch_monthly_activity(
        self, user: Any, start_date: datetime.date, end_date: datetime.date
    ):
        # 1日が日曜日までの日数を計算
        days_until_sunday = start_date.weekday()
        first_day_of_calendar = start_date - datetime.timedelta(days=days_until_sunday)

        # 月の最終日が土曜日までの日数を計算
        days_from_last_saturday = 6 - end_date.weekday()
        last_day_of_calendar = end_date + datetime.timedelta(
            days=days_from_last_saturday
        )

        activity_data_raw = ReadingMemoRepository.fetch_for_user_within_date_range(
            user, first_day_of_calendar, last_day_of_calendar
        )

        # デフォルト値を0に設定して日付ごとの辞書を作成
        activity_data_default = defaultdict(int)
        current_day = first_day_of_calendar
        while current_day <= last_day_of_calendar:
            activity_data_default[current_day] = 0
            current_day += datetime.timedelta(days=1)

        # 実際の活動データをデフォルトの辞書にマージ
        for data in activity_data_raw:
            activity_data_default[data["date_str"]] = data["count"]

        # TODO 1~5の範囲にする
        # TODO valueの値を5で割る
        activity_data = [
            {"date": key, "activity_count": self._calc_level(value)}
            for key, value in activity_data_default.items()
        ]

        return activity_data

    def _calc_level(self, activity_count):
        if activity_count <= 0:
            return 0
        elif activity_count <= 5:
            return 1
        elif activity_count <= 10:
            return 2
        elif activity_count <= 15:
            return 3
        elif activity_count <= 20:
            return 4
        elif activity_count <= 25:
            return 5
        else:
            return 0
