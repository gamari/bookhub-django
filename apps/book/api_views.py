from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from apps.book.application.usecases import (
    AddBookToShelfUsecase,
    RemoveBookFromShelfUsecase,
)
from apps.book.domain.repositories import (
    BookRepository,
    BookshelfRepository,
)
from apps.book.domain.services import (
    BookDomainService,
)
from apps.record.domain.repositories import (
    ReadingRecordRepository,
)
from apps.record.domain.services import (
    RecordDomainService,
)


@login_required
def api_book_on_shelf(request, book_id):
    book_service = BookDomainService(BookRepository(), BookshelfRepository())
    reading_record_service = RecordDomainService(ReadingRecordRepository())

    if request.method == "POST":
        try:
            usecase = AddBookToShelfUsecase(book_service, reading_record_service)
            usecase.execute(book_id, request.user)
            return JsonResponse({"message": "追加に成功しました。"}, status=200)
        except Exception as e:
            return JsonResponse({"error": "本棚に追加できませんでした。"}, status=400)

    elif request.method == "DELETE":
        try:
            usecase = RemoveBookFromShelfUsecase(book_service)
            usecase.execute(book_id, request.user)
            return JsonResponse({"message": "削除に成功しました。"}, status=200)
        except Exception as e:
            return JsonResponse({"error": "本棚から削除できませんでした。"}, status=400)

    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
