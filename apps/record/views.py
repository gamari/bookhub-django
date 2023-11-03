from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

from apps.book.models import Book
from apps.record.application.usecases import (
    RecordReadingHistoryUsecase,
)
from apps.record.models import ReadingRecord


@login_required
def reading_record_page(request, book_id):
    usecase = RecordReadingHistoryUsecase.build()

    context = usecase.execute(book_id, request.user)

    return render(request, "reading_record.html", context)


# TODO 移動させてAPIViewで書き換える
# API系
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
