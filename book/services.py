from collections import defaultdict
from typing import Any
from abc import ABC, abstractmethod
import datetime
from datetime import timedelta

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import Count, Avg
from django.db.models.functions import TruncDate

from book.apis import GoogleBooksAPIClient
from book.mappers import GoogleBooksMapper
from book.models import Bookshelf
from book.repositories import BookRepository

from record.models import ReadingMemo
from review.forms import ReviewForm


class SearchService(ABC):
    @abstractmethod
    def search(self, query, page):
        pass


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


class BookApplicationService:
    def __init__(self, book_service):
        self.book_service = book_service

    def view_book_detail(self, book_id, user):
        book, latest_review, book_on_shelf = self.book_service.get_book_detail(
            book_id, user
        )

        avg_rating = book.review_set.aggregate(avg_rating=Avg("rating"))["avg_rating"]
        if avg_rating:
            avg_rating = round(avg_rating, 2)
        reviews = book.review_set.all().order_by("-created_at")
        context = {
            "book": book,
            "review_form": ReviewForm(
                instance=latest_review if latest_review else None
            ),
            "latest_review": latest_review,
            "avg_rating": avg_rating,
            "reviews": reviews,
            "book_on_shelf": book_on_shelf,
        }
        return context


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
            books.append(book)

        total_items = api_result.get("totalItems", 0)
        total_pages = (total_items // 10) + (1 if total_items % 10 else 1)

        return books, total_pages


# Dashboard


User = get_user_model()


class ActivityService:
    @staticmethod
    def fetch_monthly_activity(
        user: Any, start_date: datetime.date, end_date: datetime.date
    ):
        # 1日が日曜日までの日数を計算
        days_until_sunday = start_date.weekday()
        first_day_of_calendar = start_date - datetime.timedelta(days=days_until_sunday)

        # 月の最終日が土曜日までの日数を計算
        days_from_last_saturday = 6 - end_date.weekday()
        last_day_of_calendar = end_date + datetime.timedelta(
            days=days_from_last_saturday
        )

        activity_data_raw = (
            ReadingMemo.objects.filter(
                created_at__date__range=[start_date, end_date],
                user=user,
            )
            .annotate(date_str=TruncDate("created_at"))
            .values("date_str")
            .annotate(count=Count("id"))
            .values("date_str", "count")
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

        # TODO activity_countは5より小さくする
        activity_data = [
            {"date": key, "activity_count": value if value <= 5 else 5}
            for key, value in activity_data_default.items()
        ]

        return activity_data


class DashboardService:
    @staticmethod
    def prepare_dashboard_data(user: Any):
        bookshelf, created = Bookshelf.objects.get_or_create(user=user)
        books = bookshelf.books.all()

        today = timezone.now().date()
        today = timezone.now().date()
        start_date = today.replace(day=1)
        end_date = today.replace(month=today.month % 12 + 1, day=1) - timedelta(days=1)

        activity_data = ActivityService.fetch_monthly_activity(
            user, start_date, end_date
        )

        return {"books": books, "activity_data": activity_data}
