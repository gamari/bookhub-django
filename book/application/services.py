from typing import Any
from datetime import timedelta

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import Avg

from book.domain.services import ActivityService
from book.models import Bookshelf
from review.forms import ReviewForm

User = get_user_model()


class BookApplicationService:
    def __init__(self, book_service):
        self.book_service = book_service
        print("test")

    def execute(self, book_id, user):
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


class DashboardApplicationService:
    """ダッシュボード"""

    def execute(self, user: Any):
        bookshelf, created = Bookshelf.objects.get_or_create(user=user)
        books = bookshelf.books.all()

        today = timezone.now().date()
        today = timezone.now().date()
        start_date = today.replace(day=1)
        end_date = today.replace(month=today.month % 12 + 1, day=1) - timedelta(days=1)

        activity_service = ActivityService()
        activity_data = activity_service.fetch_monthly_activity(
            user, start_date, end_date
        )

        month = today.month

        return {
            "books": books,
            "activity_data": activity_data,
            "month": month,
            "bookshelf": bookshelf
        }
