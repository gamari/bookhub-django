from django.shortcuts import render


from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from book.models import Book
from record.models import ReadingRecord


@login_required
def reading_record(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    record, created = ReadingRecord.objects.get_or_create(user=request.user, book=book)

    context = {"book": book, "record": record}
    return render(request, "reading_record.html", context)
