from django.core.management.base import BaseCommand

from apps.management.application.usecases import CreateRecommendBook


class Command(BaseCommand):
    help = 'オススメの書籍を投稿します。'

    def handle(self, *args, **options):
        self.stdout.write("実行")
        usecase = CreateRecommendBook.build()
        usecase.execute()

        self.stdout.write(self.style.SUCCESS('投稿に成功しました。'))