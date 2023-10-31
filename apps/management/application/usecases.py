import logging

from config.application.usecases import Usecase
from apps.book.domain.services import BookDomainService
from config.clients import TwitterClient
from config.settings import APP_URL

logger = logging.getLogger("app_logger")

class AutoCreateRecommendBook(Usecase):
    def __init__(self, book_service):
        self.book_service = book_service

    @classmethod
    def build(cls):
        book_service = BookDomainService.initialize()

        return cls(
            book_service,
        )

    def execute(self):
        # TODO ここの精度を上げる
        random_book = self.book_service.get_random_book()

        # TODO 出来ればランダムにレビューを引用したい
        header = f"【おすすめ】\n{random_book.title}\n"

        hash_tags = f"#Yommy #本好きと繋がりたい"

        if len(random_book.title) < 25:
            hash_tags += f" #{random_book.title}"

        url = f"{APP_URL}/detail/{random_book.id}"

        content = f"{header}\n\n{hash_tags}\n\b{url}"
        logger.debug(content)

        twitter_client = TwitterClient()
        twitter_client.post_tweet(content)



