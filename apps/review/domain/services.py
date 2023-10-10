from apps.review.domain.repositories import ReviewRepository


class ReviewDomainService(object):
    """レビュードメイン。"""

    def __init__(self, review_repo: ReviewRepository):
        self.review_repo = review_repo

    def get_latest_review_for_user(self, book, user):
        if user.is_authenticated:
            return self.review_repo.fetch_latest_review_by_user(book, user)
        else:
            return None

    def get_reviews_by_user_within_this_month(self, user):
        return self.review_repo.fetch_reviews_by_user_within_this_month(user)
    
    def get_latest_reviews(self, limit):
        return self.review_repo.fetch_latest_reviews(limit)
    
    def get_latest_reviews_by_user(self, user, limit):
        return self.review_repo.fetch_latest_reviews_by_user(user, limit)
