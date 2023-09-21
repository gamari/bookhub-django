from django.db import models
from django.contrib.auth import get_user_model

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

    def __str__(self):
        return f"[{self.isbn_10} | {self.isbn_13}] {self.title}"

class Bookshelf(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)

    def add_book(self, book: Book):
        self.books.add(book)

    def remove_book(self, book: Book):
        self.books.remove(book)