from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

from book.domain.repositories import BookRepository, BookshelfRepository
from book.domain.services import BookService
from book.models import Book
from record.application.service import (
    CreateMemoApplicationService,
    ReadingApplicationService,
)
from record.domain.repositories import ReadingMemoRepository, ReadingRecordRepository
from record.domain.service import ReadingMemoService, ReadingService
from record.models import ReadingRecord
from review.repositories import ReviewRepository


@login_required
def reading_record(request, book_id):
    record_repository = ReadingRecordRepository()
    book_service = BookService(BookRepository, ReviewRepository, BookshelfRepository)
    reading_service = ReadingService(record_repository)

    service = ReadingApplicationService(
        request.user, book_id, reading_service, book_service
    )
    
    context = service.execute()

    return render(request, "reading_record.html", context)


# API
@login_required
def create_memo(request, book_id):
    if request.method == "POST":
        service = CreateMemoApplicationService(
            BookRepository, ReadingMemoRepository, ReadingMemoService
        )
        response_data = service.execute(request.POST, request.user, book_id)

        if response_data["result"] == "success":
            return JsonResponse(response_data, status=201)
        else:
            return JsonResponse(response_data, status=400)
    else:
        return JsonResponse({"result": "fail"}, status=400)


@login_required
def mark_as_finished(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    record, created = ReadingRecord.objects.get_or_create(user=request.user, book=book)
    record.mark_as_finished()
    record.save()
    return redirect("reading_record", book_id=book_id)


@login_required
def mark_as_unfinished(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    try:
        record = ReadingRecord.objects.get(user=request.user, book=book)
        record.mark_as_unfinished()
        record.save()
    except ReadingRecord.DoesNotExist:
        pass
    return redirect("reading_record", book_id=book_id)
