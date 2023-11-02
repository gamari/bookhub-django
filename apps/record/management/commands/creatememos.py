import datetime
import random
from django.core.management.base import BaseCommand
from apps.book.models import Book

from apps.management.application.usecases import CreateRecommendBook
from apps.record.models import ReadingMemo
from authentication.models import Account


class Command(BaseCommand):
    help = 'オススメの書籍を投稿します。'

    def handle(self, *args, **options):
        self.stdout.write("実行")

        user = Account.objects.filter(is_staff=True).first()
        bookshelf = user.bookshelf
        book = bookshelf.books.first()
        
        # 100回メモを作成する
        for i in range(20):
            day = random.randint(1, 29)
            hour = random.randint(1, 23)
            minute = random.randint(1, 59)
            second = random.randint(1, 59)

            created_at = datetime.datetime.now()
            created_at = created_at.replace(day=day, hour=hour, minute=minute, second=second)
            print(created_at)

            ReadingMemo.objects.create(
                user=user,
                book=book,
                content=f"メモ{i}",
                created_at=created_at
            )

        self.stdout.write(self.style.SUCCESS('投稿に成功しました。'))