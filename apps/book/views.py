from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required


from apps.book.application.usecases import (
    AddBookToShelfUsecase,
    CreateBookSelectionUsecase,
    DetailBookSelectionUsecase,
    ShowBookDetailPageUsecase,
    ShowHomePageUsecase,
    ShowMyPageUsecase,
    RemoveBookFromShelfUsecase,
)
from apps.book.domain.repositories import (
    BookRepository,
    BookSelectionRepository,
    BookshelfRepository,
)
from apps.book.forms import BookSelectionForm
from apps.book.models import BookSelection, Bookshelf
from apps.book.domain.services import (
    BookDomainService,
    BookSelectionDomainService,
    BookshelfDomainService,
)
from apps.record.domain.repositories import (
    ReadingMemoRepository,
    ReadingRecordRepository,
)
from apps.record.domain.services import (
    ActivityDomainService,
    MemoDomainService,
    RecordDomainService,
)
from apps.review.domain.repositories import ReviewRepository
from apps.review.domain.services import ReviewDomainService


def home(request):
    record_service = RecordDomainService(ReadingRecordRepository())
    review_service = ReviewDomainService(ReviewRepository())
    memo_service = MemoDomainService(ReadingMemoRepository())

    usecase = ShowHomePageUsecase(record_service, review_service, memo_service)
    context = usecase.execute()

    return render(request, "pages/home.html", context)


@login_required
def mypage(request):
    bookshelf_service = BookshelfDomainService(BookshelfRepository())
    activity_service = ActivityDomainService(ReadingMemoRepository())
    record_service = RecordDomainService(ReadingRecordRepository())
    review_service = ReviewDomainService(ReviewRepository())
    selection_service = BookSelectionDomainService(BookSelectionRepository())

    usecase = ShowMyPageUsecase(
        bookshelf_service, activity_service, record_service, review_service,selection_service
    )
    context = usecase.execute(request.user)

    return render(request, "pages/mypage.html", context)


def book_detail_page(request, book_id):
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
    # TODO 記録を削除したい
    book_service = BookDomainService(BookRepository(), BookshelfRepository())
    usecase = RemoveBookFromShelfUsecase(book_service)
    usecase.execute(book_id, request.user)

    return redirect("book_detail", book_id=book_id)


# セレクション
@login_required
def create_selection(request):
    if request.method == "POST":
        selection_service = BookSelectionDomainService(BookSelectionRepository())
        usecase = CreateBookSelectionUsecase(selection_service)
        usecase.execute(request.POST, request.user)
        return redirect("mypage")
    form = BookSelectionForm(user=request.user)
    return render(
        request,
        "pages/create_selection.html",
        {
            "form": form,
        },
    )

def selection_detail(request, selection_id):
    usecase = DetailBookSelectionUsecase(
        BookSelectionDomainService(BookSelectionRepository())
    )

    context = usecase.execute(selection_id)

    return render(
        request, 
        "pages/selection_detail.html", 
        context
    )

@login_required
def delete_selection(request, selection_id):
    selection = BookSelection.objects.get(id=selection_id)
    selection.delete()
    return redirect("mypage")