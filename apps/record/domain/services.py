import logging
from datetime import datetime
from apps.follow.models import Follow
from config.utils import DateUtils

from apps.record.domain.aggregates import ActivityCollection
from apps.record.domain.repositories import ReadingMemoRepository, ReadingRecordRepository
from apps.record.forms import ReadingMemoForm

logger = logging.getLogger("app_logger")

class RecordDomainService(object):
    """記録ドメインサービス。"""

    def __init__(self, reading_record_repo: ReadingRecordRepository) -> None:
        self.reading_record_repo = reading_record_repo

    @classmethod
    def initialize(cls):
        reading_record_repo = ReadingRecordRepository()
        return cls(reading_record_repo)
    
    def get_or_create_record(self, user, book):
        return self.reading_record_repo.fetch_or_create(user, book)
    
    def get_top_books(self, start_date, end_date, limit):
        return self.reading_record_repo.fetch_top_books(start_date, end_date, limit)
    
    def get_by_user_and_book(self, user, book):
        return self.reading_record_repo.fetch_record_by_user_and_book(user, book)
    
    def get_finished_books_this_month(self, user):
        return self.reading_record_repo.fetch_finished_books_this_month(user)


class MemoDomainService(object):
    """メモドメインサービス。"""
    def __init__(self, memo_repo: ReadingMemoRepository) -> None:
        self.memo_repo = memo_repo
    
    @classmethod
    def initialize(cls):
        memo_repo = ReadingMemoRepository()
        return cls(memo_repo)
    
    def get_memos_of_book_with_paginate(self, book, page=1):
        return self.memo_repo.fetch_memos_by_book_with_paginate(book, page)

    def get_latest_memos(self, limit: int = None):
        return self.memo_repo.fetch_latest_memos(limit)
    
    def get_memos_of_book_before_date(self, book, date, limit: int = None):
        """"""
        return self.memo_repo.fetch_memos_by_book_and_date(book, date, limit)

    def get_memos_by_user(self, user, limit: int = None):
        return self.memo_repo.fetch_memos_by_user(user, limit)
    
    def get_memos_of_followings_and_me(self, user, limit=None, since_date=None, previous_date=None):
        """ユーザーとフォローしているユーザーのメモを取得する"""
        logger.debug(f"{limit}")
        followings = Follow.objects.filter(follower=user).values_list('followed', flat=True)
        users_to_fetch = list(followings) + [user]
        order_by = '-created_at'
        return self.memo_repo.fetch_memos_for_users(users_to_fetch, limit, since_date, previous_date, order_by)

    def create_memo_from_form(self, form: ReadingMemoForm, user, book):
        # TODO DDD的にformはドメインが持つべきかを検討する
        memo = form.save(commit=False)
        memo.user = user
        memo.book = book
        memo.save()
        return memo


class ActivityDomainService(object):
    """活動履歴ドメイン"""

    def __init__(self, reading_memo_repo: ReadingMemoRepository):
        self.reading_memo_repo = reading_memo_repo
    
    @classmethod
    def initialize(cls):
        reading_memo_repo = ReadingMemoRepository()
        return cls(reading_memo_repo)

    def fetch_activities(
        self, user, start_date: datetime.date, end_date: datetime.date
    ):
        head_date_of_calendar = DateUtils.head_of_calendar(start_date)
        end_date_of_calendar = DateUtils.end_of_calendar(end_date)

        # TODO 取得できたメモだけを集計するように変更したい

        activity_data_raw = self.reading_memo_repo.fetch_memos_by_user_within_date_range(
            user, head_date_of_calendar, end_date_of_calendar
        )

        activities = ActivityCollection.from_raw_data(
            activity_data_raw, head_date_of_calendar, end_date_of_calendar
        )
        filtered_activities = activities.filter_activities()

        return filtered_activities
