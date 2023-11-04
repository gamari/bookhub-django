import logging
from django.db import IntegrityError, transaction
from apps.book.models import BookTag, Tag

# from apps.book.models import BookTag, Tag
from config.application.usecases import Usecase
from apps.book.domain.services import BookDomainService
from config.clients import TwitterClient
from config.domain.services import AiDomainService
from config.settings import APP_URL

logger = logging.getLogger("app_logger")

class CreateRecommendBook(Usecase):
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
        header = f"【アウトプットしてみませんか？】\n{random_book.title}\n"

        hash_tags = f"#Yommy #本好きと繋がりたい"

        if len(random_book.title) < 25:
            hash_tags += f" #{random_book.title}"

        url = f"{APP_URL}/detail/{random_book.id}"

        content = f"{header}\n\n{hash_tags}\n\b{url}"
        logger.debug(content)

        twitter_client = TwitterClient()
        twitter_client.post_tweet(content)

class CreateBookTagsByAIUsecase(Usecase):
    def __init__(self, book_service: BookDomainService, ai_service: AiDomainService):
        self.book_service = book_service
        self.ai_service = ai_service

    @classmethod
    def build(cls):
        book_service = BookDomainService.initialize()
        ai_service = AiDomainService.initialize()

        return cls(
            book_service,
            ai_service,
        )

    def execute(self, book_id):
        book = self.book_service.get_book_by_id(book_id)
        tags = self.ai_service.create_tags_by_book(book)
        logger.debug(f"tags: {tags}")

        with transaction.atomic():
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)

                BookTag.objects.get_or_create(book=book, tag=tag)
            


