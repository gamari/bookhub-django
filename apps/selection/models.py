import uuid
from django.db import models

from apps.book.models import Account, Book


class BookSelection(models.Model):
    id: uuid.UUID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    title = models.CharField("セレクション名", max_length=126, default="セレクション名")
    description = models.TextField("セレクション説明", null=True, blank=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="selections")
    books = models.ManyToManyField(Book, through='SelectionBookRelation', related_name="in_selections", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_likes(self):
        return self.likes.count()

class BookSelectionLike(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="selection_likes")
    selection = models.ForeignKey(BookSelection, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'selection']

# お気に入り
class BookSelectionFavorite(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="selection_favorites")
    selection = models.ForeignKey(BookSelection, on_delete=models.CASCADE, related_name="favorites")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'selection']


### 以下中間テーブル

class SelectionBookRelation(models.Model):
    """BookSelectionとBookの中間テーブル。"""
    selection = models.ForeignKey(BookSelection, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('selection', 'book')
