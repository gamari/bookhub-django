from django.shortcuts import get_object_or_404

from apps.book.models import Book
from apps.review.forms import ReviewForm
from apps.review.models import Review

class RemoveReviewUsecase(object):
    """レビューを削除する。"""

    def __init__(self, user, review_id) -> None:
        self.user = user
        self.review_id = review_id

    def execute(self):
        review = get_object_or_404(Review, id=self.review_id, user=self.user)
        review.delete()
        return {"message": "Review deleted successfully."}, 200



class ReviewUsecase(object):
    """レビューする。"""

    def __init__(self, user, book_id, post_data) -> None:
        self.user = user
        self.book_id = book_id
        self.post_data = post_data

    def execute(self):
        book = get_object_or_404(Book, id=self.book_id)

        existing_review = Review.objects.filter(user=self.user, book=book).first()

        form = ReviewForm(self.post_data, instance=existing_review)

        if form.is_valid():
            review = form.save(commit=False)
            if not existing_review:
                review.user = self.user
                review.book = book
            review.save()
            return {"message": "Review submitted successfully."}, 200
        else:
            return {"error": "Invalid form submission."}, 400
