import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Avg


User = get_user_model()


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    isbn_10 = models.CharField(max_length=10, unique=True, null=True, blank=True)
    isbn_13 = models.CharField(max_length=13, unique=True, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    authors = models.ManyToManyField(Author)
    thumbnail = models.URLField(null=True, blank=True)
    published_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"[{self.isbn_10} | {self.isbn_13}] {self.title}"

    def get_avg_rating(self):
        """書籍の平均評価を取得する。"""
        return round(
            self.review_set.aggregate(avg_rating=Avg("rating"))["avg_rating"], 2
        )

    def get_reviews(self):
        """書籍のレビューを取得する。"""
        return self.review_set.all().order_by("-created_at")


class Bookshelf(models.Model):
    id: uuid.UUID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)

    def add_book(self, book: Book):
        self.books.add(book)

    def remove_book(self, book: Book):
        self.books.remove(book)
