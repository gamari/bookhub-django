import logging

from django.core.management.base import BaseCommand

from apps.management.models import Tweet, TweetTag
from config.clients import TwitterClient
from config.settings import DEBUG

logger = logging.getLogger("app_logger")

class Command(BaseCommand):
    help = 'オススメの書籍を投稿します。'

    def handle(self, *args, **options):
        self.stdout.write("実行")
        
        
        tweet = Tweet.objects.filter(is_active=True).order_by("?").first()
        content = tweet.content
        
        tags = TweetTag.objects.all().order_by("?")[:3]
        tags_str = "".join([f"#{tag.title} " for tag in tags])
        
        content = f"{content}\n{tags_str}"
        
        if DEBUG:
            logger.debug(content)
        else:
            twitter_client = TwitterClient()
            twitter_client.post_tweet(content)

        self.stdout.write(self.style.SUCCESS('ツイートしました。'))