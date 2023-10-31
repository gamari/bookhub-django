import logging, re

from apps.book.domain.services import BookDomainService, BookshelfDomainService
from apps.book.infrastructure.mappers import GoogleBooksMapper

from apps.search.infrastracture.external.apis import GoogleBooksAPIClient

from apps.selection.domain.services import BookSelectionDomainService
from apps.selection.models import BookSelectionLike
from config.application.usecases import Usecase
from config.domain.services import AiDomainService
from config.exceptions import ApplicationException
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




class AICreateSelectionUsecase(Usecase):
    """
    AIが要求からセレクションの作成をしてくれる機能。

    {"demand": "謎解きのある作品が読みたいです。"}
    """
    def __init__(self) -> None:
        super().__init__()
    
    @classmethod
    def build(cls):
        return cls()

    def run(self, demand, user):
        if len(demand) > 100 or len(demand) < 10:
            raise ApplicationException("要望は10文字以上100文字以内で入力してください。")
        
        ai_service = AiDomainService()
        title = ai_service.create_selection_title(demand)
        logger.debug(f"title: {title}")
        
        api_client = GoogleBooksAPIClient()
        api_result = api_client.search_newest_books_by_title(title, 1, 20)
        book_items = api_result.get("items", [])

        books_data = GoogleBooksMapper.to_books(book_items)

        book_service = BookDomainService.initialize()
        books = book_service.get_or_create_books(books_data)
        logger.debug(f"{len(books)}件がヒット")
        books = [book for book in books if not book.is_sensitive]

        target = [{
            "id": book.id,
            "title": book.title,
        } for book in books]


        logger.debug(f"target: {target}")

        recommend_books_str = ai_service.recommend_books(demand, target)
        logger.debug(f"recommend_books_str: {recommend_books_str}")
        recommend_books = extract_ids_from_selection(recommend_books_str)

        if len(recommend_books) == 0:
            raise ApplicationException("おすすめの本が見つかりませんでした。")
        
        # TODO recommend_booksが空の場合の処理

        # 本棚に追加
        bookshelf_serivce = BookshelfDomainService.initialize()
        bookshelf_serivce.add_books(recommend_books, user)

        # セレクション作成
        selection_service = BookSelectionDomainService.initialize()
        selection = selection_service.create_selection_by_book_ids(demand, recommend_books, user)

        return selection
