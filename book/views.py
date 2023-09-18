import requests

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

from book.models import Book, Bookshelf
from review.forms import ReviewForm
from review.models import Review


def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    review_form = ReviewForm()

    try:
        if request.user.is_authenticated:
            latest_review = book.review_set.filter(user=request.user).latest(
                "created_at"
            )
            book_on_shelf = Bookshelf.objects.filter(
                user=request.user, books=book
            ).exists()
        else:
            latest_review = None
            book_on_shelf = False
    except Review.DoesNotExist:
        latest_review = None
        book_on_shelf = False

    if latest_review:
        review_form = ReviewForm(instance=latest_review)
    else:
        review_form = ReviewForm()

    avg_rating = book.review_set.aggregate(avg_rating=Avg("rating"))["avg_rating"]
    if avg_rating:
        avg_rating = round(avg_rating, 2)

    reviews = book.review_set.all().order_by("-created_at")

    context = {
        "book": book,
        "review_form": review_form,
        "latest_review": latest_review,
        "avg_rating": avg_rating,
        "reviews": reviews,
        "book_on_shelf": book_on_shelf,
    }
    return render(request, "books/book_detail.html", context)


def show_home(request):
    latest_reviews = Review.objects.all().order_by("-created_at")[:5]

    context = {"latest_reviews": latest_reviews}

    return render(request, "home.html", context)


@login_required
def show_dashboard(request):
    bookshelf, created = Bookshelf.objects.get_or_create(user=request.user)

    books = bookshelf.books.all()

    context = {"books": books}

    return render(request, "dashboard.html", context)


def show_book_search(request):
    query = request.GET.get("query")
    results = []

    results = Book.objects.filter(title__icontains=query)

    return render(request, "books/search_results.html", {"results": results})


# 本棚処理
@login_required
def add_to_shelf(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # ユーザーの本棚を取得するか、存在しない場合は作成します。
    shelf, created = Bookshelf.objects.get_or_create(user=request.user)

    # 本棚に書籍を追加します。
    shelf.books.add(book)

    return redirect("book_detail", book_id=book.id)


@login_required
def remove_from_shelf(request, book_id):
    book: Book = get_object_or_404(Book, id=book_id)

    shelf, created = Bookshelf.objects.get_or_create(user=request.user)

    # 本棚から書籍を排除します。
    shelf.books.remove(book)

    return redirect("book_detail", book_id=book.id)
