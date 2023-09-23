from review.models import Review


class ReviewRepository:
    @staticmethod
    def latest_review_for_user(book, user):
        try:
            return book.review_set.filter(user=user).latest("created_at")
        except Review.DoesNotExist:
            return None