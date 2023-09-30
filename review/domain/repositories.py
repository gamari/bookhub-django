from datetime import datetime, timedelta
from review.models import Review


class ReviewRepository:
    @staticmethod
    def latest_review_for_user(book, user):
        try:
            return book.review_set.filter(user=user).latest("created_at")
        except Review.DoesNotExist:
            return None

    @staticmethod
    def get_latest_reviews(limit):
        return Review.objects.all().order_by("-created_at")[:limit]

    @staticmethod
    def get_reviews_for_user_this_month(user):
        """今月のレビュー数を取得"""

        # TODO タイムゾーンがずれる

        today = datetime.today()
        first_day_of_month = today.replace(day=1, hour=0, minute=0, second=0)
        print(first_day_of_month)
        last_day_of_month = (first_day_of_month + timedelta(days=32)).replace(
            day=1,
            hour=23,
            minute=59,
            second=59,
        ) - timedelta(days=1)
        print(last_day_of_month)

        return Review.objects.filter(
            user=user, created_at__range=(first_day_of_month, last_day_of_month)
        ).count()
