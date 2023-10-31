import logging, re

from apps.book.domain.services import BookDomainService, BookshelfDomainService
from apps.book.infrastructure.mappers import GoogleBooksMapper

from apps.search.infrastracture.external.apis import GoogleBooksAPIClient
from config.clients import TwitterClient
from apps.selection.domain.services import BookSelectionDomainService
from apps.selection.models import BookSelectionLike
from config.application.usecases import Usecase
from config.domain.services import AiDomainService
from config.exceptions import ApplicationException
from config.settings import APP_URL
from config.utils import extract_ids_from_selection

logger = logging.getLogger("app_logger")

class CreateBookSelectionUsecase(Usecase):
    def __init__(self, book_selection_service: BookSelectionDomainService):
        self.book_selection_service = book_selection_service
    
    @classmethod
    def build(cls):
        book_selection_service = BookSelectionDomainService.initialize()
        return cls(book_selection_service)

    def run(self, body, user):
        return self.book_selection_service.save_selection(body, user)

class EditBookSelectionUsecase(Usecase):
    def __init__(self, book_selection_service: BookSelectionDomainService):
        self.book_selection_service = book_selection_service
    
    @classmethod
    def build(cls):
        book_selection_service = BookSelectionDomainService.initialize()
        return cls(book_selection_service)


    def run(self, body, user, selection_id):
        existing_selection = self.book_selection_service.get_selection_by_id(selection_id)
        self.book_selection_service.ensure_user_is_owner(existing_selection, user)
        return self.book_selection_service.save_selection(body, user, existing_selection)


class DetailBookSelectionUsecase(Usecase):
    def __init__(self, book_selection_service: BookSelectionDomainService):
        self.book_selection_service = book_selection_service
    
    @classmethod
    def build(cls):
        book_selection_service = BookSelectionDomainService.initialize()
        return cls(book_selection_service)

    def run(self, selection_id, user):
        selection = self.book_selection_service.get_selection_by_id(selection_id)

        if not selection.is_public and selection.user != user:
            raise ApplicationException("非公開です。")

        if user.is_authenticated:
            is_liked = BookSelectionLike.objects.filter(user=user, selection=selection).exists()
        else:
            is_liked = False
        
        selection.inclement_views()

        return {"selection": selection, "is_liked": is_liked }


class AICreateSelectionByProfile(Usecase):
    """AIのプロフィールからセレクションを作成する機能。"""

    def __init__(self, 
            ai_service: AiDomainService,
            book_service: BookDomainService,
            bookshelf_service: BookshelfDomainService, 
            selection_service: BookSelectionDomainService
        ) -> None:
        self.ai_service = ai_service
        self.book_service = book_service
        self.bookshelf_service = bookshelf_service
        self.selection_service = selection_service
    
    @classmethod
    def build(cls):
        ai_service = AiDomainService.initialize()
        book_service = BookDomainService.initialize()
        bookshelf_service = BookshelfDomainService.initialize()
        selection_service = BookSelectionDomainService.initialize()
        return cls(
            ai_service,
            book_service,
            bookshelf_service,
            selection_service
        )
    
    def run(self, ai_user):
        logger.debug(f"ai_user: {ai_user}")
        description = ai_user.description
        title = self._generate_title_from_description(description)
        logger.debug(f"title: {title}")

        book_items = self._fetch_books_from_api(title)

        books_data = GoogleBooksMapper.to_books(book_items)

        books = self.book_service.get_or_create_books(books_data)
        logger.debug(f"{len(books)}件がヒット")
        books = [book for book in books if not book.is_sensitive]

        target = [{
            "id": book.id,
            "title": book.title,
        } for book in books]


        logger.debug(f"target: {target}")

        recommend_books = self._get_recommended_books(description, books)

        # TODO recommend_book_idsが空の場合の処理
        if len(recommend_books) == 0:
            raise ApplicationException("おすすめの本が見つかりませんでした。")
        
        # タイトルを箇条書きでテキストで出す出す
        recommend_titles_str = "\n".join([book.title for book in recommend_books])
        logger.debug(f"recommend_titles_str: {recommend_titles_str}")
        selection_title = self.ai_service.create_selection_title_by_book_ids(recommend_titles_str)
        

        self.bookshelf_service.add_books(recommend_books, ai_user)
        selection = self.selection_service.create_selection_by_book_ids(selection_title, recommend_books, ai_user)

        # ツイートする
        header = f"【{selection_title}】"
        hash_tags = "#Yommy #読書好きな人と繋がりたい"
        url = f"{APP_URL}/selection/{selection.id}/"
        content = f"{header}\n\n{hash_tags}\n\n{url}"
        logger.debug(content)

        twitter_client = TwitterClient()
        twitter_client.post_tweet(content)

        return selection
    
    def _generate_title_from_description(self, description):
        title = self.ai_service.create_selection_title_by_profile(description)
        logger.debug(f"title: {title}")
        return title

    def _fetch_books_from_api(self, title):
        api_client = GoogleBooksAPIClient()
        api_result = api_client.search_newest_books_by_title(title, 1, 20)
        return api_result.get("items", [])
    
    def _get_recommended_books(self, description, books):
        target = [{"id": book.id, "title": book.title} for book in books]
        logger.debug(f"target: {target}")
        
        recommend_books_str = self.ai_service.recommend_books_by_profile(description, target)
        logger.debug(f"recommend_books_str: {recommend_books_str}")
        
        recommend_book_ids = extract_ids_from_selection(recommend_books_str)
        logger.debug(f"recommend_book_ids: {recommend_book_ids}")
        
        return [book for book in books if book.id in recommend_book_ids]


class AICreateSelectionUsecaseByDemand(Usecase):
    """
    AIが要求からセレクションの作成をしてくれる機能。

    {"demand": "謎解きのある作品が読みたいです。"}
    """
    def __init__(
        self, 
        ai_service: AiDomainService, 
        book_service: BookDomainService,
        bookshelf_service: BookshelfDomainService, 
        selection_service: BookSelectionDomainService
    ):
        self.ai_service = ai_service
        self.book_service = book_service
        self.bookshelf_service = bookshelf_service
        self.selection_service = selection_service
    
    @classmethod
    def build(cls):
        ai_service = AiDomainService.initialize()
        book_service = BookDomainService.initialize()
        bookshelf_service = BookshelfDomainService.initialize()
        selection_service = BookSelectionDomainService.initialize()
        return cls(
            ai_service=ai_service, 
            book_service=book_service,
            bookshelf_service=bookshelf_service,
            selection_service=selection_service
        )

    def run(self, demand, user):
        if len(demand) > 100 or len(demand) < 10:
            raise ApplicationException("要望は10文字以上100文字以内で入力してください。")
        
        title = self.ai_service.create_selection_title_by_demand(demand)
        logger.debug(f"title: {title}")
        
        api_client = GoogleBooksAPIClient() # TODO service層だよね
        api_result = api_client.search_newest_books_by_title(title, 1, 20)
        book_items = api_result.get("items", [])

        books_data = GoogleBooksMapper.to_books(book_items)

        books = self.book_service.get_or_create_books(books_data)
        logger.debug(f"{len(books)}件がヒット")
        books = [book for book in books if not book.is_sensitive]

        target = [{
            "id": book.id,
            "title": book.title,
        } for book in books]


        logger.debug(f"target: {target}")

        recommend_books_str = self.ai_service.recommend_books_by_demand(demand, target)
        logger.debug(f"recommend_books_str: {recommend_books_str}")
        recommend_book_ids = extract_ids_from_selection(recommend_books_str)
        logger.debug(f"recommend_book_ids: {recommend_book_ids}")
        # booksからrecommend_book_idsのものを取り出す
        recommend_books = [book for book in books if book.id in recommend_book_ids]
        logger.debug(f"recommend_books: {recommend_books}")

        if len(recommend_books) == 0:
            raise ApplicationException("おすすめの本が見つかりませんでした。")
        
        # TODO recommend_book_idsが空の場合の処理

        title = "AIによるセレクション"
        self.bookshelf_service.add_books(recommend_books, user)
        selection = self.selection_service.create_selection_by_book_ids(title, recommend_books, user)

        return selection
