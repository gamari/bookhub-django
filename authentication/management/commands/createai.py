from django.core.management.base import BaseCommand, CommandError

from authentication.models import Account

class Command(BaseCommand):
    help = 'AIユーザーを作成します。'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='AIユーザーの名前')
        
        parser.add_argument('description', type=str, help='AIユーザーの説明')

    def handle(self, *args, **options):
        username = options['username']
        description = options['description']
        
        if not username or not description:
            raise CommandError('ユーザー名と説明は必須です。')

        self.stdout.write(f"createai 実行: {username} - {description}")

        count = Account.objects.all().filter(is_ai=True).count()

        newAccount = Account.objects.create_user(
            username=f"{username}",
            email=f"{username}{count}",
            description=description,
            is_ai=True,
        )

        self.stdout.write(self.style.SUCCESS('createai SUCCESS'))
