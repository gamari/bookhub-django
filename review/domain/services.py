class ReviewDomainService(object):
    """レビュードメイン。"""

    def __init__(self, review_repo):
        self.review_repo = review_repo

    def latest_review_for_user(self, book, user):
        if user.is_authenticated:
            return self.review_repo.latest_review_for_user(book, user)
        else:
            return None