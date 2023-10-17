import uuid
from django.db import models

from apps.book.models import Account, Book


class BookSelection(models.Model):
    """書籍セレクション。"""

    id: uuid.UUID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    title = models.CharField("セレクション名", max_length=126, default="セレクション名")
    description = models.TextField("セレクション説明", null=True, blank=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="selections")
    books = models.ManyToManyField(Book, related_name="in_selections", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

