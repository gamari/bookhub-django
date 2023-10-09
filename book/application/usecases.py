from django.utils import timezone
from book.domain.repositories import BookshelfRepository
from config.application.usecases import Usecase

from config.utils import get_month_date_range, get_month_range_of_today
from book.models import Bookshelf
from ranking.models import WeeklyRanking, WeeklyRankingEntry
from record.domain.repositories import ReadingRecordRepository
from record.domain.services import ActivityDomainService
from review.forms import ReviewForm
from review.domain.repositories import ReviewRepository


class HomePageShowUsecase(Usecase):
    """ホーム画面を表示する。"""

    def __init__(
        self,
        record_repo: ReadingRecordRepository,
        review_repo: ReviewRepository,
    ) -> None:
        self.record_repo = record_repo
        self.review_repo = review_repo

    def run(self) -> dict:
        first_day_of_month, last_day_of_month = get_month_range_of_today()
        top_book_results = self.record_repo.get_top_books(
            first_day_of_month, last_day_of_month, limit=3
        )
        latest_reviews = self.review_repo.get_latest_reviews(limit=5)

        # ランキングを取得する
        # TODO リファクタリングする
        try:
            latest_ranking = WeeklyRanking.objects.latest("end_date")

            if latest_ranking is None:
                ranking_entries = None
            else:
                ranking_entries = WeeklyRankingEntry.objects.filter(
                    ranking=latest_ranking
                ).order_by("-added_count")
        except:
            ranking_entries = None

        context = {
            "top_book_results": top_book_results,
            "reviews": latest_reviews,
            "ranking_entries": ranking_entries,
            "rating_range": range(1, 6),
        }

        return context


class MyPageShowUsecase(Usecase):
    """マイページを表示する。"""

    def __init__(
        self,
        user,
        bookshelf_repository: BookshelfRepository,
        activity_service: ActivityDomainService,
        record_repo: ReadingRecordRepository,
        review_repo: ReviewRepository,
    ) -> None:
        self.user = user
        self.bookshelf_repository = bookshelf_repository
        self.activity_service = activity_service
        self.record_repo = record_repo
        self.review_repo = review_repo

    def run(self):
        bookshelf: Bookshelf = self.bookshelf_repository.get_or_create(user=self.user)
        books = bookshelf.get_books_with_reading_records(self.user)

        today = timezone.now().date()

        start_date, end_date = get_month_date_range(today)

        activity_data = self.activity_service.fetch_activities(
            self.user, start_date, end_date
        )

        finished_count = self.record_repo.finished_books_this_month(self.user)

        reviews_count = self.review_repo.get_reviews_for_user_this_month(self.user)

        month = today.month

        return {
            "books": books,
            "activity_data": activity_data,
            "month": month,
            "bookshelf": bookshelf,
            "finished_count": finished_count,
            "reviews_count": reviews_count,
        }


class BookDetailPageShowUsecase(Usecase):
    """書籍詳細画面を表示する。"""

    def __init__(self, book_id, user, book_service):
        self.book_id = book_id
        self.user = user
        self.book_service = book_service

    def run(self):
        book = self.book_service.find_book_by_id(self.book_id)

        # 閲覧数のカウントアップ
        book.views += 1
        book.save()

        latest_review = (
            book.get_reviews().first() if book.get_reviews().exists() else None
        )
        avg_rating = book.get_avg_rating()
        reviews = book.get_reviews()
        book_on_shelf = self.book_service.is_book_on_shelf(book, self.user)
        registers = Bookshelf.objects.filter(books__id=book.id).count()

        context = {
            "book": book,
            "review_form": ReviewForm(instance=latest_review),
            "latest_review": latest_review,
            "avg_rating": avg_rating,
            "reviews": reviews,
            "book_on_shelf": book_on_shelf,
            "rating_range": range(1, 6),
            "reviews_count": reviews.count(),
            "registers": registers,
        }
        return context
