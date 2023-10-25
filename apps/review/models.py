import logging

from django.db import models
from django.contrib.auth import get_user_model

from apps.book.models import Book

rating_choices = [(i, str(i)) for i in range(1, 6)]

User = get_user_model()

logger = logging.getLogger("app_logger")

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        choices=rating_choices, 
        default=5
    )
    content = models.TextField(max_length=2000, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"[{self.user}] {self.content}"

    class Meta:
        unique_together = ("user", "book")
    
    def is_latest(self):
        return self == self.book.get_reviews().first()
    
    @property
    def like_count(self):
        return self.reviewlike_set.count()
    
    def is_liked_by(self, user):
        return ReviewLike.objects.filter(user=user, review=self).exists()



class ReviewLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "review")