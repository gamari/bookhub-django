from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required


from book.application.usecases import (
    BookDetailPageShowUsecase,
    HomePageShowUsecase,
    MyPageShowUsecase,
)
from book.domain.repositories import BookRepository, BookshelfRepository
from book.models import Book, Bookshelf
from book.domain.services import (
    BookDomainService,
)
from record.domain.repositories import ReadingRecordRepository
from record.domain.services import ActivityDomainService
from review.domain.repositories import ReviewRepository


def home(request):
    usecase = HomePageShowUsecase(ReadingRecordRepository(), ReviewRepository())
    context = usecase.execute()
    return render(request, "home.html", context)


@login_required
def mypage(request):
    # TODO repository -> serviceにリファクタリングしたい
    usecase = MyPageShowUsecase(
        request.user,
        BookshelfRepository(),
        ActivityDomainService(),
        ReadingRecordRepository(),
        ReviewRepository(),
    )
    context = usecase.execute()
    return render(request, "mypage.html", context)


# 書籍詳細
def book_detail(request, book_id):
    book_service = BookDomainService(BookRepository(), BookshelfRepository())
    usecase = BookDetailPageShowUsecase(book_id, request.user, book_service)
    context = usecase.execute()
    return render(request, "books/book_detail.html", context)


# 本棚
def bookshelf_list(request, bookshelf_id):
    bookshelf = Bookshelf.objects.get(id=bookshelf_id)
    return render(request, "bookshelf_list.html", {"bookshelf": bookshelf})


@login_required
def add_book_to_shelf(request, book_id):
    book: Book = get_object_or_404(Book, id=book_id)
    shelf, created = Bookshelf.objects.get_or_create(user=request.user)
    shelf.books.add(book)

    return redirect("book_detail", book_id=book.id)


@login_required
def remove_book_from_shelf(request, book_id):
    book: Book = get_object_or_404(Book, id=book_id)

    shelf, created = Bookshelf.objects.get_or_create(user=request.user)

    shelf.books.remove(book)

    return redirect("book_detail", book_id=book.id)
