from datetime import datetime, timedelta

from django.db.models import Avg
from django.utils import timezone
from django.db.models import Count
from book.domain.repositories import BookshelfRepository
from book.domain.services import ActivityService

from config.utils import get_month_date_range
from book.models import Bookshelf
from record.models import ReadingRecord
from review.forms import ReviewForm
from review.models import Review


class HomePageShowUsecase(object):
    """ホーム画面を表示する。"""

    def __init__(self) -> None:
        pass

    def execute(self) -> dict:
        # 今月の最初の日を取得
        first_day_of_month = datetime.now().replace(day=1)

        # 今月の最後の日を取得
        last_day_of_month = first_day_of_month.replace(
            month=first_day_of_month.month % 12 + 1, day=1
        ) - timedelta(days=1)

        # 今月に登録されたReadingRecordをフィルタリング
        monthly_records = ReadingRecord.objects.filter(
            started_at__range=[first_day_of_month, last_day_of_month]
        )

        # 書籍ごとにエントリーを集計
        top_book_results = (
            monthly_records.values("book__title", "book__id", "book__thumbnail")
            .annotate(total=Count("book"))
            .order_by("-total")[:3]
        )
        print(top_book_results)

        latest_reviews = Review.objects.all().order_by("-created_at")[:5]

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
        bookshelf: Bookshelf = self.get_or_create_bookshelf()
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

    def get_or_create_bookshelf(self):
        return self.bookshelf_repository.get_or_create(user=self.user)


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
