from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

from apps.book.models import Book
from apps.record.application.usecases import (
    CreateMemoUsecase,
    DeleteMemoUsecase,
    RecordReadingHistoryUsecase,
)
from apps.record.domain.repositories import ReadingMemoRepository
from apps.record.models import ReadingRecord


@login_required
def reading_record_page(request, book_id):
    usecase = RecordReadingHistoryUsecase.build()

    context = usecase.execute(book_id, request.user)

    return render(request, "reading_record.html", context)


# TODO 移動させてAPIViewで書き換える
# API系
@login_required
def create_memo_api(request, book_id):
    if request.method == "POST":
        usecase = CreateMemoUsecase.build()

        response_data = usecase.run(request.POST, request.user, book_id)

        if response_data["result"] == "success":
            return JsonResponse(response_data, status=201)
        else:
            return JsonResponse(response_data, status=400)
    else:
        return JsonResponse({"result": "fail"}, status=400)


@login_required
def memo_detail_api(request, memo_id):
    if request.method == "DELETE":
        usecase = DeleteMemoUsecase(memo_id, request.user, ReadingMemoRepository())
        response_data = usecase.execute()

        if response_data["result"] == "success":
            return JsonResponse(response_data, status=201)
        else:
            return JsonResponse(response_data, status=400)


# 開始操作
@login_required
def mark_as_started(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    record, created = ReadingRecord.objects.get_or_create(user=request.user, book=book)
    record.mark_as_started()
    record.save()
    return redirect("reading_record", book_id=book_id)


@login_required
def mark_as_unstarted(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    try:
        record = ReadingRecord.objects.get(user=request.user, book=book)
        record.mark_as_unstarted()
        record.save()
    except ReadingRecord.DoesNotExist:
        pass
    return redirect("reading_record", book_id=book_id)


@login_required
def mark_as_finished(request, book_id):
    # TODO usecaseに切り出す
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
