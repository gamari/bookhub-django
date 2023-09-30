import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Avg


User = get_user_model()


class Author(models.Model):
    """著者。"""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    """書籍。"""

    id = models.AutoField(primary_key=True)
    isbn_10 = models.CharField(max_length=10, unique=True, null=True, blank=True)
    isbn_13 = models.CharField(max_length=13, unique=True, null=True, blank=True)
    title = models.CharField("書籍名", max_length=255)
    description = models.TextField("書籍説明", null=True, blank=True)
    authors = models.ManyToManyField(Author)
    thumbnail = models.URLField("サムネイル", null=True, blank=True)
    published_date = models.DateField("出版日", null=True, blank=True)
    publisher = models.CharField("出版社", max_length=255, null=True, blank=True)

    def __str__(self):
        return f"[{self.isbn_10} | {self.isbn_13}] {self.title}"

    def get_avg_rating(self):
        """書籍の平均評価を取得する。"""
        avg_rating = self.review_set.aggregate(avg_rating=Avg("rating"))["avg_rating"]
        return round(avg_rating, 2) if avg_rating is not None else None

    def get_reviews(self):
        """書籍のレビューを取得する。"""
        return self.review_set.all().order_by("-created_at")


class Bookshelf(models.Model):
    """本棚。"""

    id: uuid.UUID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, through="BookshelfBook")

    def add_book(self, book: Book):
        self.books.add(book)

    def remove_book(self, book: Book):
        self.books.remove(book)


class BookshelfBook(models.Model):
    """中間テーブル"""

    bookshelf = models.ForeignKey(Bookshelf, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
