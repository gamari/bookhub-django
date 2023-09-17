import requests

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from book.apis import GoogleBooksAPI


def book_detail(request, book_id):
    book_api = GoogleBooksAPI()

    book = book_api.get_detail(book_id)
    return render(request, "books/book_detail.html", {"book": book})


def show_home(request):
    return render(request, "home.html")


@login_required
def show_dashboard(request):
    print(request.user)
    return render(request, "dashboard.html")


def show_book_search(request):
    query = request.GET.get("q")
    results = []

    book_api = GoogleBooksAPI()

    if query:
        results = book_api.search(query)

    return render(request, "books/search_results.html", {"results": results})
