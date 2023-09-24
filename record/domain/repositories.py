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
    def get_or_create(self, user, book):
        return ReadingRecord.objects.get_or_create(user=user, book=book)
