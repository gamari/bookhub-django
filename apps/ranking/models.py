from django.db import models
import uuid

from apps.book.models import Book


class WeeklyRanking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)


class WeeklyRankingEntry(models.Model):
    ranking = models.ForeignKey(
        WeeklyRanking, related_name="entries", on_delete=models.CASCADE
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-added_count"]
