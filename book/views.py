from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required


from book.application.usecases import (
    AddBookToShelfUsecase,
    BookDetailPageShowUsecase,
    ShowHomePageUsecase,
    ShowMyPageUsecase,
    RemoveBookFromShelfUsecase,
)
from book.domain.repositories import BookRepository, BookshelfRepository
from book.models import Book, Bookshelf
from book.domain.services import (
    BookDomainService,
    BookshelfDomainService,
)
from record.domain.repositories import ReadingMemoRepository, ReadingRecordRepository
from record.domain.services import ActivityDomainService, RecordDomainService
from review.domain.repositories import ReviewRepository
from review.domain.services import ReviewDomainService


def home(request):
    usecase = ShowHomePageUsecase(ReadingRecordRepository(), ReviewRepository())
    context = usecase.execute()
    return render(request, "pages/home.html", context)


@login_required
def mypage(request):
    bookshelf_service = BookshelfDomainService(BookshelfRepository())
    activity_service = ActivityDomainService(
        ReadingMemoRepository()
    )
    record_service = RecordDomainService(ReadingRecordRepository())
    review_service = ReviewDomainService(ReviewRepository())

    usecase = ShowMyPageUsecase(
        bookshelf_service,
        activity_service,
        record_service,
        review_service
    )
    context = usecase.execute(request.user)

    return render(request, "pages/mypage.html", context)


# 書籍詳細
def book_detail_page(request, book_id):
    book_service = BookDomainService(BookRepository(), BookshelfRepository())

    usecase = BookDetailPageShowUsecase(book_service)
    context = usecase.execute(book_id, request.user)

    return render(request, "pages/book_detail.html", context)


# 本棚
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
    # TODO 記録を削除したい
    book_service = BookDomainService(BookRepository(), BookshelfRepository())
    usecase = RemoveBookFromShelfUsecase(book_service)
    usecase.execute(book_id, request.user)

    return redirect("book_detail", book_id=book_id)
