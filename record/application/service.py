from django.shortcuts import get_object_or_404

from book.models import Book
from record.forms import ReadingMemoForm
from record.models import ReadingMemo


class ReadingApplicationService:
    def __init__(self, user, book_id, reading_service):
        self.user = user
        self.book_id = book_id
        self.reading_service = reading_service

    def execute(self):
        book = get_object_or_404(Book, id=self.book_id)
        record = self.reading_service.get_or_create_record(self.user, book)
        memos = ReadingMemo.objects.filter(user=self.user, book=book).order_by(
            "-created_at"
        )
        form = ReadingMemoForm()
        return {"book": book, "record": record, "memos": memos, "form": form}
