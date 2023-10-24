from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test

from apps.book.models import Book

@user_passes_test(lambda u: u.is_superuser)
def management_dashboard(request):
    context = {}
    return render(request, "pages/manage-dashboard.html", context)

@user_passes_test(lambda u: u.is_superuser)
def management_books(request):
    books = Book.objects.all().filter(is_clean=False).order_by("-views")[:10]
    context = {
        "books": books,
    }
    return render(request, "pages/manage-books.html", context)

# 書籍編集ページ
@user_passes_test(lambda u: u.is_superuser)
def management_book_edit(request, book_id):
    book = Book.objects.get(id=book_id)
    context = {
        "book": book,
    }
    return render(request, "pages/manage-book-edit.html", context)