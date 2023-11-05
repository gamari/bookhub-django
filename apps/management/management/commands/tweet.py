import logging

from django.core.management.base import BaseCommand

from apps.management.models import Tweet
from config.clients import TwitterClient

logger = logging.getLogger("app_logger")

class Command(BaseCommand):
    help = 'オススメの書籍を投稿します。'

    def handle(self, *args, **options):
        self.stdout.write("実行")
        tweet = Tweet.objects.filter(is_active=True).order_by("?").first()
        logger.debug(tweet.content)      
        
        twitter_client = TwitterClient()
        twitter_client.post_tweet(tweet.content)

        self.stdout.write(self.style.SUCCESS('ツイートしました。'))