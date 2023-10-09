from datetime import date

from django.db import models
from django.contrib.auth import get_user_model

from book.models import Book


User = get_user_model()


# TODO 紐づけ先をReadingRecordにすべき
class ReadingMemo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)


class ReadingRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    started_at = models.DateField(null=True, blank=True)
    finished_at = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"[{self.finished_at}]{self.user}は{self.book}を読んでいます"

    def mark_as_started(self):
        self.started_at = date.today()

    def mark_as_unstarted(self):
        self.started_at = None

    def mark_as_finished(self):
        self.finished_at = date.today()

    def mark_as_unfinished(self):
        self.finished_at = None
