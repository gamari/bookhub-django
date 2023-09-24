from django.http import JsonResponse
from django.shortcuts import render


from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from book.models import Book
from record.application.service import ReadingApplicationService
from record.domain.repositories import ReadingRecordRepository
from record.domain.service import ReadingService
from record.forms import ReadingMemoForm


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
    # TODO 返ってくる日付がUTCを考慮してない
    book = get_object_or_404(Book, id=book_id)
    response_data = {}

    if request.method == "POST":
        form = ReadingMemoForm(request.POST)
        if form.is_valid():
            memo = form.save(commit=False)
            memo.user = request.user
            memo.book = book
            memo.save()
            response_data["result"] = "success"
            response_data["content"] = memo.content
            response_data["created_at"] = memo.created_at.strftime("%Y-%m-%d %H:%M:%S")
        else:
            response_data["result"] = "fail"
            response_data["errors"] = form.errors

    return JsonResponse(response_data)
