import requests

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from book.models import Book
from review.forms import ReviewForm


def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    review_form = ReviewForm()

    context = {
        "book": book,
        "review_form": review_form,
    }
    return render(request, "books/book_detail.html", context)


def show_home(request):
    return render(request, "home.html")


@login_required
def show_dashboard(request):
    print(request.user)
    return render(request, "dashboard.html")


def show_book_search(request):
    query = request.GET.get("q")
    results = []

    results = Book.objects.filter(title__icontains=query)

    return render(request, "books/search_results.html", {"results": results})
