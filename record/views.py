from django.http import JsonResponse
from django.shortcuts import render


from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from book.models import Book
from record.forms import ReadingMemoForm
from record.models import ReadingMemo, ReadingRecord

# TODO book_idで指定するのは直観的ではない

@login_required
def reading_record(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    record, created = ReadingRecord.objects.get_or_create(user=request.user, book=book)
    memos = ReadingMemo.objects.filter(user=request.user, book=book).order_by(
        "-created_at"
    )
    form = ReadingMemoForm()

    context = {"book": book, "record": record, "memos": memos, "form": form}
    return render(request, "reading_record.html", context)


@login_required
def create_memo(request, book_id):
    print("メモ")
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
