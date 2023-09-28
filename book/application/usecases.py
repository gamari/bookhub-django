from django.db.models import Avg
from django.utils import timezone
from book.domain.repositories import BookshelfRepository
from book.domain.services import ActivityService

from config.utils import get_month_date_range, get_month_range_of_today
from book.models import Bookshelf
from record.domain.repositories import ReadingRecordRepository
from review.forms import ReviewForm
from review.repositories import ReviewRepository


class HomePageShowUsecase(object):
    """ホーム画面を表示する。"""

    def __init__(
        self, record_repo: ReadingRecordRepository, review_repo: ReviewRepository
    ) -> None:
        self.record_repo = record_repo
        self.review_repo = review_repo

    def execute(self) -> dict:
        first_day_of_month, last_day_of_month = get_month_range_of_today()
        top_book_results = self.record_repo.get_top_books(
            first_day_of_month, last_day_of_month, limit=3
        )
        latest_reviews = self.review_repo.get_latest_reviews(limit=5)

        context = {
            "top_book_results": top_book_results,
            "latest_reviews": latest_reviews,
        }

        return context


class MyPageShowUsecase(object):
    """マイページを表示する。"""

    def __init__(
        self,
        user,
        bookshelf_repository: BookshelfRepository,
        activity_service: ActivityService,
    ) -> None:
        self.user = user
        self.bookshelf_repository = bookshelf_repository
        self.activity_service = activity_service

    def execute(self):
        bookshelf: Bookshelf = self.bookshelf_repository.get_or_create(user=self.user)
        books = bookshelf.books.all()

        today = timezone.now().date()

        start_date, end_date = get_month_date_range(today)

        activity_data = self.activity_service.fetch_monthly_activity(
            self.user, start_date, end_date
        )

        month = today.month

        return {
            "books": books,
            "activity_data": activity_data,
            "month": month,
            "bookshelf": bookshelf,
        }


class BookDetailPageShowUsecase(object):
    """書籍詳細画面を表示する。"""

    def __init__(self, book_id, user, book_service):
        self.book_id = book_id
        self.user = user
        self.book_service = book_service

    def execute(self):
        book, latest_review, book_on_shelf = self.book_service.get_book_detail(
            self.book_id, self.user
        )

        avg_rating = book.review_set.aggregate(avg_rating=Avg("rating"))["avg_rating"]
        if avg_rating:
            avg_rating = round(avg_rating, 2)
        reviews = book.review_set.all().order_by("-created_at")
        context = {
            "book": book,
            "review_form": ReviewForm(
                instance=latest_review if latest_review else None
            ),
            "latest_review": latest_review,
            "avg_rating": avg_rating,
            "reviews": reviews,
            "book_on_shelf": book_on_shelf,
        }
        return context


class BookSearchUsecase(object):
    """書籍検索を行う。"""

    def __init__(self, mode, page, query, search_service) -> None:
        self.mode = mode
        self.page = page
        self.query = query
        self.search_service = search_service

    def execute(self):
        results_list, total_pages = self.search_service.search(self.query, self.page)

        context = {
            "results": results_list,
            "query": self.query,
            "current_page": self.page,
            "total_pages": total_pages,
            "mode": self.mode,
        }

        return context
