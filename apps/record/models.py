import logging
from datetime import date

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.book.models import Book


User = get_user_model()

logger = logging.getLogger("app_logger")

# TODO 紐づけ先をReadingRecordにすべき
class ReadingMemo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(default=timezone.now)
    
    def get_isoformat_created_at(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M:%S')

class ReadingRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    started_at = models.DateField(null=True, blank=True)
    finished_at = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        unique_together = ("user", "book")

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
