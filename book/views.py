from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from book.domain.repositories import BookRepository, BookshelfRepository
from book.application.services import (
    BookApplicationService,
    DashboardApplicationService,
)
from book.models import Book, Bookshelf
from book.domain.services import (
    BookSearchService,
    BookService,
    GoogleBooksService,
)
from record.models import ReadingRecord
from review.models import Review
from review.repositories import ReviewRepository


# ページ表示
def home(request):
    # 今月の最初の日を取得
    first_day_of_month = datetime.now().replace(day=1)

    # 今月の最後の日を取得
    last_day_of_month = first_day_of_month.replace(
        month=first_day_of_month.month % 12 + 1, day=1
    ) - timedelta(days=1)

    # 今月に登録されたReadingRecordをフィルタリング
    monthly_records = ReadingRecord.objects.filter(
        started_at__range=[first_day_of_month, last_day_of_month]
    )

    # 書籍ごとにエントリーを集計
    top_book_results = (
        monthly_records.values(
            "book__title", "book__id", "book__thumbnail"
        )  # book__titleで書籍のタイトルを使用
        .annotate(total=Count("book"))
        .order_by("-total")[:3]
    )
    print(top_book_results)

    latest_reviews = Review.objects.all().order_by("-created_at")[:5]

    context = {
        "top_book_results": top_book_results,
        "latest_reviews": latest_reviews,
    }

    return render(request, "home.html", context)


@login_required
def dashboard(request):
    service = DashboardApplicationService()
    context = service.execute(request.user)
    return render(request, "dashboard.html", context)


# 書籍詳細
def book_detail(request, book_id):
    book_service = BookService(BookRepository, ReviewRepository, BookshelfRepository)
    service = BookApplicationService(book_service)
    context = service.execute(book_id, request.user)
    return render(request, "books/book_detail.html", context)


# 検索
def book_search(request):
    query = request.GET.get("query")
    mode = request.GET.get("mode", "")
    page = int(request.GET.get("page", 1))

    # TODO 詳細検索は、ログイン時のみ利用可能にする

    if mode == "detail":
        search_service = GoogleBooksService()
    else:
        search_service = BookSearchService()

    results_list, total_pages = search_service.search(query, page)

    context = {
        "results": results_list,
        "query": query,
        "current_page": page,
        "total_pages": total_pages,
        "mode": mode,
    }

    return render(request, "books/search_results.html", context)


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

    shelf.books.remove(book)

    return redirect("book_detail", book_id=book.id)
