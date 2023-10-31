from django.core.management.base import BaseCommand
from apps.selection.application.usecases import AICreateSelectionByProfile
from authentication.models import Account

from config.settings import OPEN_AI_KEY

class Command(BaseCommand):
    help = 'AIがセレクションを作ります。'

    def handle(self, *args, **options):
        self.stdout.write("実行")

        print(OPEN_AI_KEY)

        # AIユーザーをランダムに取得
        ai_user = Account.objects.all().filter(is_ai=True).order_by('?').first()

        # 1. 作成する
        usecase = AICreateSelectionByProfile.build()
        usecase.execute(ai_user)

        # 2. セレクションをツイートする

        self.stdout.write(self.style.SUCCESS('作成に成功しました。'))