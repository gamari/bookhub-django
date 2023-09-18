from collections import defaultdict
import math
import requests
from datetime import date, timedelta, datetime
from calendar import monthrange

from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.db.models import Count
from django.db.models.functions import TruncDate

from book.models import Book, Bookshelf
from record.forms import ReadingMemoForm
from record.models import ReadingMemo
from review.forms import ReviewForm
from review.models import Review


def show_book_detail(request, book_id):
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


@login_required
def show_dashboard(request):
    bookshelf, created = Bookshelf.objects.get_or_create(user=request.user)
    books = bookshelf.books.all()

    # 活動履歴の処理
    today = timezone.now().date()
    first_day_of_month = today.replace(day=1)
    last_day_of_month = today.replace(month=today.month % 12 + 1, day=1) - timedelta(
        days=1
    )

    # 1日が日曜日までの日数を計算
    days_until_sunday = first_day_of_month.weekday()
    first_day_of_calendar = first_day_of_month - timedelta(days=days_until_sunday)

    # 月の最終日が土曜日までの日数を計算
    days_from_last_saturday = 6 - last_day_of_month.weekday()
    last_day_of_calendar = last_day_of_month + timedelta(days=days_from_last_saturday)


    activity_data_raw = (
        ReadingMemo.objects.filter(
            created_at__date__range=[first_day_of_month, last_day_of_month],
            user=request.user,
        )
        .annotate(date_str=TruncDate("created_at"))
        .values("date_str")
        .annotate(count=Count("id"))
        .values("date_str", "count")
    )

    # デフォルト値を0に設定して日付ごとの辞書を作成
    activity_data_default = defaultdict(int)
    current_day = first_day_of_calendar
    while current_day <= last_day_of_calendar:
        activity_data_default[current_day] = 0
        current_day += timedelta(days=1)

    # 実際の活動データをデフォルトの辞書にマージ
    for data in activity_data_raw:
        activity_data_default[data["date_str"]] = data["count"]

    # TODO activity_countは5より小さくする
    activity_data = [
        {"date": key, "activity_count": value if value <= 5 else 5}
        for key, value in activity_data_default.items()
    ]

    context = {"books": books, "activity_data": activity_data}

    return render(request, "dashboard.html", context)


def show_home(request):
    latest_reviews = Review.objects.all().order_by("-created_at")[:5]

    context = {"latest_reviews": latest_reviews}

    return render(request, "home.html", context)


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
