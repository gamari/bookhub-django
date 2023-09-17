from django.contrib import admin

from book.models import Author, Book

admin.site.register(Book)
admin.site.register(Author)