from collections import defaultdict
from typing import Any
from abc import ABC, abstractmethod
import datetime
from datetime import timedelta

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models.functions import TruncDate
from django.db.models import Count

from book.models import Bookshelf
from book.repositories import BookRepository, GoogleBooksRepository
from record.models import ReadingMemo


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
        total_pages = (total_results // 10) + (1 if total_results % 10 else 0)
        return results_list[(page-1)*10:page*10], total_results, total_pages



class GoogleBooksService(SearchService):
    def __init__(self):
        self.repository = GoogleBooksRepository()

    def search(self, query, page):
        results_list, total_results = self.repository.search_books(query, page)
        total_pages = (total_results // 10) + (1 if total_results % 10 else 0)
        return results_list, total_results, total_pages


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
