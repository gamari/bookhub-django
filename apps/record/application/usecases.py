import logging

from config.application.usecases import Usecase
from apps.book.domain.repositories import BookRepository
from apps.book.domain.services import BookDomainService
from apps.record.domain.repositories import ReadingMemoRepository
from apps.record.domain.services import MemoDomainService, RecordDomainService
from apps.record.forms import ReadingMemoForm
from apps.record.models import ReadingMemo
from apps.review.domain.services import ReviewDomainService
from apps.review.forms import ReviewForm


logger = logging.getLogger("app_logger")

class RecordReadingHistoryUsecase(Usecase):
    """読書記録画面を表示する。"""

    def __init__(
        self,
        reading_record_service: RecordDomainService,
        book_service: BookDomainService,
        review_service: ReviewDomainService,
    ):
        self.reading_record_service = reading_record_service
        self.book_service = book_service
        self.review_service = review_service

    @classmethod
    def build(cls):
        reading_record_service = RecordDomainService.initialize()
        book_service = BookDomainService.initialize()
        review_service = ReviewDomainService.initialize()

        return cls(
            reading_record_service,
            book_service,
            review_service,
        )

    def run(self, book_id, user):
        book = self.book_service.get_book_by_id(book_id)

        latest_review = self.review_service.get_latest_review_for_user(book, user)
        record = self.reading_record_service.get_or_create_record(user, book)

        memos = ReadingMemo.objects.filter(user=user, book=book).order_by("-created_at")
        form = ReadingMemoForm()

        return {
            "book": book,
            "record": record,
            "memos": memos,
            "form": form,
            "review": latest_review,
            "review_form": ReviewForm(
                instance=latest_review if latest_review else None
            ),
        }


class CreateMemoUsecase(Usecase):
    """メモ作成。"""

    def __init__(
        self,
        book_repo: BookRepository,
        memo_service: MemoDomainService,
    ):
        self.book_repo = book_repo
        self.memo_service = memo_service
    
    @classmethod
    def build(cls):
        book_repo = BookRepository()
        memo_service = MemoDomainService(ReadingMemoRepository())

        return cls(
            book_repo,
            memo_service,
        )

    def run(self, form_data, user, book_id):
        form = ReadingMemoForm(form_data)
        if not form.is_valid():
            return { "result": "fail", "errors": form.errors}

        book = self.book_repo.find_by_id(book_id)
        memo: ReadingMemo = self.memo_service.create_memo_from_form(form, user, book)

        book = self.book_repo.find_by_id(book_id)
        book_detail = {
            "id": book.id,
            "title": book.title,
            "thumbnail": book.thumbnail if book.thumbnail else None,
        }

        user = {
            "id": memo.user.id,
            "username": memo.user.username,
            "profile_image": memo.user.profile_image.url if memo.user.profile_image else None,
        }

        return {
            "id": memo.id,
            "result": "success",
            "content": memo.content,
            "created_at": memo.created_at.strftime("%Y年%m月%d日%H:%M"),
            "user": user,
            "book": book_detail
        }


class DeleteMemoUsecase(Usecase):
    """メモ削除。"""

    def __init__(self, memo_id, user, memo_repo: ReadingMemoRepository):
        self.memo_id = memo_id
        self.memo_repo = memo_repo
        self.user = user

    def execute(self):
        memo = self.memo_repo.fetch_memo_by_id(self.memo_id)

        if memo.user != self.user:
            return {"result": "fail"}

        self.memo_repo.delete(memo)
        return {"result": "success"}
