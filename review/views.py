# TODO
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect

from book.models import Book
from review.forms import ReviewForm
from review.models import Review


def create_review(request, book_id):
    book: Book = get_object_or_404(Book, id=book_id)
    existing_review = Review.objects.filter(user=request.user, book=book).first()
    
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            if not existing_review:
                review.user = request.user
                review.book = book
            review.save()
            return redirect("book_detail", book_id=book.id) # type: ignore
    return HttpResponseBadRequest("無効なリクエスト")