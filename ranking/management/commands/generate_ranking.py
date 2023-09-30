from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.db import models

from book.models import Book, BookshelfBook
from ranking.models import WeeklyRanking, WeeklyRankingEntry


class Command(BaseCommand):
    help = "Generate weekly ranking"

    def handle(self, *args, **kwargs):
        generate_weekly_ranking()
        self.stdout.write(self.style.SUCCESS("Successfully generated weekly ranking"))


def generate_weekly_ranking():
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday(), weeks=1)
    # end_of_week = start_of_week + timedelta(days=6)
    end_of_week = today

    entries_last_week = BookshelfBook.objects.filter(
        created_at__range=[start_of_week, end_of_week]
    )

    book_counts = (
        entries_last_week.values("book")
        .annotate(added_count=models.Count("book"))
        .order_by("-added_count")[:10]
    )

    weekly_ranking = WeeklyRanking.objects.create(
        start_date=start_of_week, end_date=end_of_week
    )

    for book_count in book_counts:
        book = Book.objects.get(id=book_count["book"])
        WeeklyRankingEntry.objects.create(
            ranking=weekly_ranking, book=book, added_count=book_count["added_count"]
        )
