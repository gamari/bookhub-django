import requests

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.core.paginator import Paginator

from book.application_services import DashboardService
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


@login_required
def dashboard(request):
    context = DashboardService.prepare_dashboard_data(request.user)
    return render(request, "dashboard.html", context)


def show_home(request):
    latest_reviews = Review.objects.all().order_by("-created_at")[:5]

    context = {"latest_reviews": latest_reviews}

    return render(request, "home.html", context)


# TODO 抜き出す
def search_google_books_api(query):
    GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes?q={}"
    response = requests.get(GOOGLE_BOOKS_API_URL.format(query))
    if response.status_code == 200:
        data = response.json()
        return data.get("items", [])
    return []


def book_search(request):
    query = request.GET.get("query")
    results_list = list(Book.objects.filter(title__icontains=query))

    if not results_list:
        # データベースに結果がない場合、Google Books APIを使用
        api_results = search_google_books_api(query)
        for item in api_results:
            volume_info = item.get("volumeInfo", {})
            book, created = Book.objects.get_or_create(
                title=volume_info.get("title", "Unknown Title"),
                description=volume_info.get("description", ""),
                thumbnail=volume_info.get("imageLinks", {}).get("thumbnail", "")
            )
            results_list.append(book)
    
    paginator = Paginator(results_list, 10)  # 10は1ページあたりのアイテム数。変更可。
    page = request.GET.get('page')
    results = paginator.get_page(page)

    return render(request, "books/search_results.html", {"results": results_list})


# 本棚処理
@login_required
def bookshelf(request, book_id):
    book: Book = get_object_or_404(Book, id=book_id)
    shelf, created = Bookshelf.objects.get_or_create(user=request.user)
    shelf.books.add(book)

    return redirect("book_detail", book_id=book.id)


@login_required
def remove_from_shelf(request, book_id):
    book: Book = get_object_or_404(Book, id=book_id)

    shelf, created = Bookshelf.objects.get_or_create(user=request.user)

    # 本棚から書籍を排除します。
    shelf.books.remove(book)

    return redirect("book_detail", book_id=book.id)
