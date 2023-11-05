from django.db import models
from django.contrib.auth import get_user_model

from apps.book.models import Book

Account = get_user_model()

class Note(models.Model):
    """
    書籍に対するノート。
    """
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=10000, blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)