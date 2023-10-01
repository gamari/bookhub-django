from datetime import timedelta, date, datetime, timedelta
from typing import List, Dict
from collections import defaultdict
from config.utils import DateUtils
from record.domain.aggregates import ActivityCollection

from record.domain.repositories import ReadingMemoRepository


class ReadingService:
    """読書ドメイン"""

    def __init__(self, record_repository):
        self.record_repository = record_repository

    def get_or_create_record(self, user, book):
        return self.record_repository.get_or_create(user, book)


class ReadingMemoService:
    """メモドメイン"""

    @staticmethod
    def create_memo(form, user, book):
        memo = form.save(commit=False)
        memo.user = user
        memo.book = book
        return memo


# 活動履歴ドメイン


class ActivityDomainService:
    def fetch_activities(
        self, user, start_date: datetime.date, end_date: datetime.date
    ):
        head_date_of_calendar = DateUtils.head_of_calendar(start_date)
        end_date_of_calendar = DateUtils.end_of_calendar(end_date)

        # TODO 取得できたメモだけを集計するように変更したい

        activity_data_raw = ReadingMemoRepository.fetch_for_user_within_date_range(
            user, head_date_of_calendar, end_date_of_calendar
        )

        activities = ActivityCollection.from_raw_data(
            activity_data_raw, head_date_of_calendar, end_date_of_calendar
        )
        filtered_activities = activities.filter_activities()

        return filtered_activities
