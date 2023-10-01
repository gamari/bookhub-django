from abc import ABC, abstractmethod
from collections import defaultdict
import datetime
from typing import Any

from record.domain.repositories import ReadingMemoRepository


# 書籍ドメイン
class BookDomainService:
    def __init__(self, book_repository, bookshelf_repository):
        self.book_repository = book_repository
        self.bookshelf_repository = bookshelf_repository

    def find_book_by_id(self, book_id: int):
        """書籍IDから書籍を取得する。"""
        return self.book_repository.find_by_id(book_id)

    def is_book_on_shelf(self, book, user):
        """書籍が本棚に含まれているかどうかを判定する。"""
        if not user.is_authenticated:
            return False
        return self.bookshelf_repository.has_book_for_user(book, user)
    
    def get_or_create_books(self, books_data):
        """書籍一覧を取得または作成する。"""
        books = []
        for book_data in books_data:
            book = self.book_repository.get_or_create(book_data)
            if book:
                books.append(book)
        return books



# 活動履歴ドメイン

class ActivityDomainService:
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
