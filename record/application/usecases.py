from book.domain.repositories import BookRepository

from record.domain.repositories import ReadingMemoRepository
from record.domain.services import ReadingMemoService
from record.forms import ReadingMemoForm
from record.models import ReadingMemo
from review.domain.services import ReviewDomainService
from review.forms import ReviewForm


class RecordReadingHistoryUsecase(object):
    """読書記録画面を表示する。"""

    def __init__(
        self,
        user,
        book_id,
        reading_service: ReadingMemoService,
        book_service,
        review_service: ReviewDomainService,
    ):
        self.user = user
        self.book_id = book_id
        self.reading_service = reading_service
        self.book_service = book_service
        self.review_service = review_service

    def execute(self):
        book = self.book_service.find_book_by_id(self.book_id)

        latest_review = self.review_service.latest_review_for_user(book, self.user)

        record, created = self.reading_service.get_or_create_record(self.user, book)
        memos = ReadingMemo.objects.filter(user=self.user, book=book).order_by(
            "-created_at"
        )
        form = ReadingMemoForm()
        return {
            "book": book,
            "record": record,
            "memos": memos,
            "form": form,
            "review_form": ReviewForm(
                instance=latest_review if latest_review else None
            ),
        }


class CreateMemoUsecase(object):
    """メモ作成。"""

    def __init__(
        self,
        book_repo: BookRepository,
        memo_repo: ReadingMemoRepository,
        memo_service: ReadingMemoService,
    ):
        self.book_repo = book_repo
        self.memo_repo = memo_repo
        self.memo_service = memo_service

    def execute(self, form_data, user, book_id):
        form = ReadingMemoForm(form_data)
        if not form.is_valid():
            return {"result": "fail", "errors": form.errors}

        book = self.book_repo.find_by_id(book_id)
        memo = self.memo_service.create_memo(form, user, book)
        saved_memo = self.memo_repo.save(memo)

        return {
            "result": "success",
            "content": saved_memo.content,
            "created_at": saved_memo.created_at.strftime("%Y年%m月%d日 %H:%M"),
        }
