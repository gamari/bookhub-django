from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required


from book.application.usecases import (
    BookDetailPageShowUsecase,
    BookSearchUsecase,
    HomePageShowUsecase,
    MyPageShowUsecase,
)
from book.domain.repositories import BookRepository, BookshelfRepository
from book.models import Book, Bookshelf
from book.domain.services import (
    ActivityService,
    BookSearchService,
    BookService,
    GoogleBooksService,
)
from record.domain.repositories import ReadingRecordRepository
from review.repositories import ReviewRepository


def home(request):
    usecase = HomePageShowUsecase(ReadingRecordRepository(), ReviewRepository())
    context = usecase.execute()
    return render(request, "home.html", context)


@login_required
def mypage(request):
    service = MyPageShowUsecase(request.user, BookshelfRepository(), ActivityService())
    context = service.execute()
    return render(request, "dashboard.html", context)


# 書籍詳細
def book_detail(request, book_id):
    book_service = BookService(
        BookRepository(), ReviewRepository(), BookshelfRepository()
    )
    usecase = BookDetailPageShowUsecase(book_id, request.user, book_service)
    context = usecase.execute()
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

    usecase = BookSearchUsecase(mode, page, query, search_service)
    context = usecase.execute()

    return render(request, "books/search_results.html", context)


# 本棚
def bookshelf_list(request, bookshelf_id):
    user_bookshelf = Bookshelf.objects.get(id=bookshelf_id)
    return render(request, "bookshelf_list.html", {"bookshelf": user_bookshelf})


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
