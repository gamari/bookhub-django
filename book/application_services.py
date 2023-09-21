from datetime import timedelta
from typing import Any

from django.utils import timezone

from book.domain_services import ActivityService

from book.models import Bookshelf


class DashboardService:
    @staticmethod
    def prepare_dashboard_data(user: Any):
        bookshelf, created = Bookshelf.objects.get_or_create(user=user)
        books = bookshelf.books.all()

        today = timezone.now().date()
        today = timezone.now().date()
        start_date = today.replace(day=1)
        end_date = today.replace(month=today.month % 12 + 1, day=1) - timedelta(
            days=1
        )

        activity_data = ActivityService.fetch_monthly_activity(
            user, start_date, end_date
        )

        return {"books": books, "activity_data": activity_data}
