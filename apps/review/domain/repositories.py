from datetime import datetime, timedelta

from apps.review.models import Review


class ReviewRepository(object):
    def fetch_latest_review_by_user(self, book, user):
        try:
            return book.review_set.filter(user=user).latest("created_at")
        except Review.DoesNotExist:
            return None

    def fetch_latest_reviews(self, limit):
        return Review.objects.all().filter(user__is_active=True).order_by("-created_at")[:limit]
    
    def fetch_latest_reviews_by_user(self, user, limit):
        return Review.objects.filter(user=user).order_by("-created_at")[:limit]

    def fetch_reviews_by_user_within_this_month(self, user):
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
