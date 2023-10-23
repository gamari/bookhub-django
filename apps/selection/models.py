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


# TODO お気に入り機能
# class FavoriteSelection(models.Model):
#     id: uuid.UUID = models.UUIDField(
#         primary_key=True, default=uuid.uuid4, editable=False
#     )
#     user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="favorite_selections")
#     book_selection = models.ForeignKey(BookSelection, on_delete=models.CASCADE, related_name="favorited_by")

#     class Meta:
#         unique_together = ('user', 'book_selection')

# # TODO いいね機能
# class LikeSelection(models.Model):
#     id: uuid.UUID = models.UUIDField(
#         primary_key=True, default=uuid.uuid4, editable=False
#     )
#     user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="liked_selections")
#     book_selection = models.ForeignKey(BookSelection, on_delete=models.CASCADE, related_name="liked_by")

#     class Meta:
#         unique_together = ('user', 'book_selection')


### 以下中間テーブル

class SelectionBookRelation(models.Model):
    """BookSelectionとBookの中間テーブル。"""
    selection = models.ForeignKey(BookSelection, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        unique_together = ('selection', 'book')
