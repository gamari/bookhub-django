from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from apps.book.application.usecases import (
    AddBookToShelfUsecase,
    ShowBookDetailPageUsecase,
    ShowHomePageUsecase,
    ShowMyPageUsecase,
    RemoveBookFromShelfUsecase,
)
from apps.book.domain.repositories import (
    BookRepository,
    BookshelfRepository,
)
from apps.book.models import Bookshelf
from apps.book.domain.services import (
    BookDomainService,
)
from apps.record.domain.repositories import (
    ReadingRecordRepository,
)
from apps.record.domain.services import (
    RecordDomainService,
)
from apps.review.domain.repositories import ReviewRepository
from apps.review.domain.services import ReviewDomainService


def home(request):
    usecase = ShowHomePageUsecase.build()
    context = usecase.execute()

    return render(request, "pages/home.html", context)


@login_required
def mypage(request):
    usecase = ShowMyPageUsecase.build()
    context = usecase.execute(request.user)

    return render(request, "pages/mypage.html", context)


def book_detail_page(request, book_id):
    """書籍詳細"""
    book_service = BookDomainService(BookRepository(), BookshelfRepository())
    review_service = ReviewDomainService(ReviewRepository())

    usecase = ShowBookDetailPageUsecase(book_service, review_service)
    context = usecase.execute(book_id, request.user)

    return render(request, "pages/book_detail.html", context)


def bookshelf_list_page(request, bookshelf_id):
    bookshelf = Bookshelf.objects.get(id=bookshelf_id)
    return render(request, "bookshelf_list.html", {"bookshelf": bookshelf})


@login_required
def add_book_to_shelf(request, book_id):
    book_service = BookDomainService(BookRepository(), BookshelfRepository())
    reading_record_service = RecordDomainService(ReadingRecordRepository())

    usecase = AddBookToShelfUsecase(book_service, reading_record_service)
    usecase.execute(book_id, request.user)

    return redirect("book_detail", book_id=book_id)


@login_required
def remove_book_from_shelf(request, book_id):
    book_service = BookDomainService(BookRepository(), BookshelfRepository())
    usecase = RemoveBookFromShelfUsecase(book_service)
    usecase.execute(book_id, request.user)

    return redirect("book_detail", book_id=book_id)


