from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255)


class Book(models.Model):
    isbn_10 = models.CharField(max_length=10, unique=True, null=True, blank=True)
    isbn_13 = models.CharField(max_length=13, unique=True, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    authors = models.ManyToManyField(Author)
    thumbnail = models.URLField(null=True, blank=True)


