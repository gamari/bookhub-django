from datetime import datetime, timedelta
from django.db.models import Count
from django.db.models.functions import TruncDate

from apps.record.models import ReadingMemo, ReadingRecord


class ReadingMemoRepository(object):
    def fetch_memos_by_user_within_date_range(self, user, start_date, end_date):
        """指定した期間内のメモを取得する"""
        return (
            ReadingMemo.objects.filter(
                created_at__date__range=[start_date, end_date],
                user=user,
            )
            .annotate(date_str=TruncDate("created_at"))
            .values("date_str")
            .annotate(count=Count("id"))
            .values("date_str", "count")
        )

    def fetch_memos(self, limit):
        return ReadingMemo.objects.filter(user__is_active=True).order_by("-created_at")[:limit]

    def fetch_memo_by_id(self, memo_id):
        return ReadingMemo.objects.get(id=memo_id)

    
    def fetch_memos_by_user(self, user, limit):
        return ReadingMemo.objects.filter(user=user).order_by("-created_at")[:limit]

    def delete(self, memo):
        memo.delete()

    def save(self, memo):
        memo.save()
        return memo


class ReadingRecordRepository(object):
    def fetch_or_create(self, user, book):
        return ReadingRecord.objects.get_or_create(user=user, book=book)

    def fetch_record_by_user_and_book(self, user, book):
        return ReadingRecord.objects.get(book=book, user=user)

    def fetch_top_books(self, start_date, end_date, limit):
        """指定した期間内の読書記録を集計し、上位の本を返す"""
        monthly_records = ReadingRecord.objects.filter(
            started_at__range=[start_date, end_date]
        )

        return (
            monthly_records.values("book__title", "book__id", "book__thumbnail")
            .annotate(total=Count("book"))
            .order_by("-total")[:limit]
        )

    def fetch_finished_books_this_month(self, user):
        """今月読み終わった本の数を返す"""
        today = datetime.today()
        first_day_of_month = today.replace(day=1)
        last_day_of_month = (first_day_of_month + timedelta(days=32)).replace(
            day=1
        ) - timedelta(days=1)
        return ReadingRecord.objects.filter(
            user=user, finished_at__range=(first_day_of_month, last_day_of_month)
        ).count()
