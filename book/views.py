import requests

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

from book.models import Book
from review.forms import ReviewForm
from review.models import Review


def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    review_form = ReviewForm()

    try:
        if request.user.is_authenticated:
            latest_review = book.review_set.filter(user=request.user).latest('created_at')
        else:
            latest_review = None
    except Review.DoesNotExist:
        latest_review = None

    if latest_review:
        review_form = ReviewForm(instance=latest_review)
    else:
        review_form = ReviewForm()

    # 平均レビュー点を計算
    avg_rating = book.review_set.aggregate(avg_rating=Avg('rating'))['avg_rating']
    if avg_rating:
        avg_rating = round(avg_rating, 2)  # 2桁の小数点で丸める

    # レビューの一覧を取得
    reviews = book.review_set.all().order_by('-created_at')

    context = {
        "book": book,
        "review_form": review_form,
        "latest_review": latest_review,
        "avg_rating": avg_rating,
        "reviews": reviews
    }
    return render(request, "books/book_detail.html", context)



def show_home(request):
    latest_reviews = Review.objects.all().order_by('-created_at')[:5]

    context = {
        "latest_reviews": latest_reviews
    }
    return render(request, "home.html", context)


@login_required
def show_dashboard(request):
    print(request.user)
    return render(request, "dashboard.html")


def show_book_search(request):
    query = request.GET.get("query")
    results = []

    results = Book.objects.filter(title__icontains=query)

    return render(request, "books/search_results.html", {"results": results})
