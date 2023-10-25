import logging

from django.utils import timezone

from config.utils import DateUtils
from config.application.usecases import Usecase
from apps.ranking.domain.services import RankingDomainService
from apps.selection.application.usecases import BookSelectionDomainService
from apps.book.domain.services import BookDomainService, BookshelfDomainService
from apps.book.models import Bookshelf
from apps.record.domain.services import (
    ActivityDomainService,
    MemoDomainService,
    RecordDomainService,
)
from apps.review.domain.services import ReviewDomainService
from apps.review.forms import ReviewForm

logger = logging.getLogger("app_logger")


class ShowHomePageUsecase(Usecase):
    """ホーム画面を表示する。"""

    @classmethod
    def build(cls):
        record_service = RecordDomainService.initialize()
        review_service = ReviewDomainService.initialize()
        memo_service = MemoDomainService.initialize()
        ranking_service = RankingDomainService.initialize()

        return cls(
            record_service,
            review_service,
            memo_service,
            ranking_service,
        )

    def __init__(
        self,
        record_service: RecordDomainService,
        review_service: ReviewDomainService,
        memo_service: MemoDomainService,
        ranking_service: RankingDomainService,
    ):
        self.record_service = record_service
        self.review_service = review_service
        self.memo_service = memo_service
        self.ranking_service = ranking_service

    def run(self):
        first_day_of_month, last_day_of_month = DateUtils.get_month_range_of_today()
        top_book_results = self.record_service.get_top_books(
            first_day_of_month, last_day_of_month, limit=3
        )
        latest_reviews = self.review_service.get_latest_reviews(limit=3)
        ranking_entries = self.ranking_service.get_latest_ranking_entries()
        memos = self.memo_service.get_memos(limit=4)

        context = {
            "top_book_results": top_book_results,
            "reviews": latest_reviews,
            "ranking_entries": ranking_entries,
            "memos": memos,
        }

        return context


class ShowMyPageUsecase(Usecase):
    """マイページを表示する。"""

    @classmethod
    def build(cls):
        bookshelf_service = BookshelfDomainService.initialize()
        activity_service = ActivityDomainService.initialize()
        record_service = RecordDomainService.initialize()
        review_service = ReviewDomainService.initialize()
        selection_service = BookSelectionDomainService.initialize()
        memo_service = MemoDomainService.initialize()

        return cls(
            bookshelf_service,
            activity_service,
            record_service,
            review_service,
            selection_service,
            memo_service
        )

    def __init__(
        self,
        bookshelf_service: BookshelfDomainService,
        activity_service: ActivityDomainService,
        record_service: RecordDomainService,
        review_service: ReviewDomainService,
        selection_service: BookSelectionDomainService,
        memo_service: MemoDomainService,
    ):
        self.bookshelf_service = bookshelf_service
        self.activity_service = activity_service
        self.record_service = record_service
        self.review_service = review_service
        self.selection_service = selection_service
        self.memo_service = memo_service

    def run(self, user):
        today = timezone.now().date()
        month = today.month
        start_date, end_date = DateUtils.get_month_date_range(today)

        bookshelf, books = self._fetch_book_data(user)
        activity_data, reviews_count, finished_count = self._fetch_activity_data(
            user, start_date, end_date
        )
        reviews = self._fetch_review_data(user)
        following_count, follower_count = self._fetch_follow_data(user)
        selections = self._fetch_selection_data(user)
        memos = self._fetch_timeline_data(user)


        return {
            "books": books,
            "activity_data": activity_data,
            "month": month,
            "bookshelf": bookshelf,
            "finished_count": finished_count,
            "reviews_count": reviews_count,
            "reviews": reviews,
            "following_count": following_count,
            "follower_count": follower_count,
            "selections": selections,
            "today": today,
            "memos": memos,
        }
    
    def _fetch_book_data(self, user):
        bookshelf = self.bookshelf_service.get_or_create(user=user)
        books = bookshelf.get_books_with_reading_records(user)
        return bookshelf, books

    def _fetch_activity_data(self, user, start_date, end_date):
        activity = self.activity_service.fetch_activities(user, start_date, end_date)
        reviews_count = self.review_service.get_reviews_by_user_within_this_month(user)
        finished_count = self.record_service.get_finished_books_this_month(user)
        return activity, reviews_count, finished_count
    
    def _fetch_review_data(self, user):
        reviews = self.review_service.get_latest_reviews_by_user(user, 5)
        return reviews

    def _fetch_follow_data(self, user):
        following_count = user.following.count()
        follower_count = user.followers.count()
        return following_count, follower_count

    def _fetch_selection_data(self, user):
        selections = self.selection_service.get_selections_for_user(user)
        return selections
    
    def _fetch_timeline_data(self, user):
        memos = self.memo_service.get_memos_of_user_and_followings(user, limit=5)
        return memos


class ShowBookDetailPageUsecase(Usecase):
    """書籍詳細画面を表示する。"""

    def __init__(
        self, book_service: BookDomainService, review_service: ReviewDomainService
    ):
        self.book_service = book_service
        self.review_service = review_service

    @classmethod
    def build(cls):
        book_service = BookDomainService.initialize()
        review_service = ReviewDomainService.initialize()

        return cls(book_service, review_service)

    def run(self, book_id, user):
        book = self.book_service.find_book_by_id(book_id)

        latest_review = self.review_service.get_latest_review_for_user(book, user)
        avg_rating = book.get_avg_rating()
        reviews = book.get_reviews(user)
        book_on_shelf = self.book_service.is_book_on_shelf(book, user)
        registers = Bookshelf.objects.filter(books__id=book.id).count()

        # 閲覧数のカウントアップ
        book.views += 1
        book.save()
        
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


class AddBookToShelfUsecase(Usecase):
    """本棚に本を追加する。"""

    def __init__(
        self,
        book_service: BookDomainService,
        reading_record_service: RecordDomainService,
    ):
        self.book_service = book_service
        self.reading_record_service = reading_record_service
    
    @classmethod
    def build(cls):
        book_service = BookDomainService.initialize()
        reading_record_service = RecordDomainService.initialize()

        return cls(book_service, reading_record_service)

    def run(self, book_id, user):
        book = self.book_service.find_book_by_id(book_id)
        bookshelf: Bookshelf = self.book_service.get_or_create_bookshelf(user)
        bookshelf.books.add(book)

        # 登録時にRecordを作成する
        record = self.reading_record_service.get_or_create_record(user, book)
        logger.info(f"{record}")

        return {}


class RemoveBookFromShelfUsecase(Usecase):
    """本棚から本を削除する。"""

    def __init__(self, book_service: BookDomainService):
        self.book_service = book_service
    
    @classmethod
    def build(cls):
        book_service = BookDomainService.initialize()

        return cls(book_service)

    def run(self, book_id, user):
        book = self.book_service.find_book_by_id(book_id)

        bookshelf: Bookshelf = self.book_service.get_or_create_bookshelf(user)
        bookshelf.books.remove(book)

        return {}
