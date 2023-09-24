from django.http import JsonResponse
from django.shortcuts import render

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from book.domain.repositories import BookRepository
from record.application.service import (
    CreateMemoApplicationService,
    ReadingApplicationService,
)
from record.domain.repositories import ReadingMemoRepository, ReadingRecordRepository
from record.domain.service import ReadingMemoService, ReadingService


@login_required
def reading_record(request, book_id):
    record_repository = ReadingRecordRepository()
    reading_service = ReadingService(record_repository)
    service = ReadingApplicationService(
        user=request.user, book_id=book_id, reading_service=reading_service
    )
    context = service.execute()
    return render(request, "reading_record.html", context)


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
