from django.db.models import Count
from django.db.models.functions import TruncDate

from record.models import ReadingMemo, ReadingRecord


class ReadingMemoRepository:
    @staticmethod
    def fetch_for_user_within_date_range(user, start_date, end_date):
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

    @staticmethod
    def save(memo):
        memo.save()
        return memo


class ReadingRecordRepository:
    @staticmethod
    def get_or_create(user, book):
        return ReadingRecord.objects.get_or_create(user=user, book=book)

    @staticmethod
    def get_top_books(start_date, end_date, limit):
        monthly_records = ReadingRecord.objects.filter(
            started_at__range=[start_date, end_date]
        )

        return (
            monthly_records.values("book__title", "book__id", "book__thumbnail")
            .annotate(total=Count("book"))
            .order_by("-total")[:limit]
        )
