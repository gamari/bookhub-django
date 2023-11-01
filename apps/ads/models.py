from django.db import models

from apps.book.models import Book

# TODO bookのIDを入力して、おすすめの本を登録する
class RecommendBook(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)