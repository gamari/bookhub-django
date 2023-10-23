from django.db import models
from django.contrib.auth import get_user_model

from apps.book.models import Book

rating_choices = [(i, str(i)) for i in range(1, 6)]

User = get_user_model()


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        choices=rating_choices, default=3
    )
    content = models.TextField(max_length=2000, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"[{self.user}] {self.content}"

    class Meta:
        unique_together = ("user", "book")
    
    def is_latest(self):
        return self == self.book.get_reviews().first()
