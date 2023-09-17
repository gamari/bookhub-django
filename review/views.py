# TODO
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect

from book.models import Book
from review.forms import ReviewForm


def create_review(request, book_id):
    book: Book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book = book
            review.save()
            return redirect("book_detail", book_id=book.id) # type: ignore
    return HttpResponseBadRequest("無効なリクエスト")
