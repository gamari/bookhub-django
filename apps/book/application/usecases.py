from django.utils import timezone
from apps.book.forms import BookSelectionForm
from config.exceptions import ApplicationException

from config.utils import DateUtils
from config.application.usecases import Usecase

from apps.book.domain.services import BookDomainService, BookSelectionDomainService, BookshelfDomainService
from apps.book.models import Bookshelf
from apps.record.domain.services import (
    ActivityDomainService,
    MemoDomainService,
    RecordDomainService,
)
from apps.review.domain.services import ReviewDomainService
from apps.review.forms import ReviewForm
from apps.ranking.models import WeeklyRanking, WeeklyRankingEntry


class ShowHomePageUsecase(Usecase):
    """ホーム画面を表示する。"""

    def __init__(
        self,
        record_service: RecordDomainService,
        review_service: ReviewDomainService,
        memo_service: MemoDomainService,
    ):
        self.record_service = record_service
        self.review_service = review_service
        self.memo_service = memo_service

    def run(self):
        first_day_of_month, last_day_of_month = DateUtils.get_month_range_of_today()
        top_book_results = self.record_service.get_top_books(
            first_day_of_month, last_day_of_month, limit=3
        )
        latest_reviews = self.review_service.get_latest_reviews(limit=3)

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

        memos = self.memo_service.get_memos(limit=4)

        context = {
            "top_book_results": top_book_results,
            "reviews": latest_reviews,
            "ranking_entries": ranking_entries,
            "rating_range": range(1, 6),
            "memos": memos,
        }

        return context


class ShowMyPageUsecase(Usecase):
    """マイページを表示する。"""

    def __init__(
        self,
        bookshelf_service: BookshelfDomainService,
        activity_service: ActivityDomainService,
        record_service: RecordDomainService,
        review_service: ReviewDomainService,
        selection_service: BookSelectionDomainService,
    ):
        self.bookshelf_service = bookshelf_service
        self.activity_service = activity_service
        self.record_service = record_service
        self.review_service = review_service
        self.selection_service = selection_service

    def run(self, user):
        # 書籍関連
        bookshelf = self.bookshelf_service.get_or_create(user=user)
        books = bookshelf.get_books_with_reading_records(user)

        # 日付関連
        today = timezone.now().date()
        month = today.month
        start_date, end_date = DateUtils.get_month_date_range(today)

        activity_data = self.activity_service.fetch_activities(
            user, start_date, end_date
        )

        finished_count = self.record_service.get_finished_books_this_month(user)

        # レビュー関連
        reviews_count = self.review_service.get_reviews_by_user_within_this_month(user)
        reviews = self.review_service.get_latest_reviews_by_user(user, 5)

        # フォロー関係
        following_count = user.following.count()
        follower_count = user.followers.count()

        # セレクション
        selections = self.selection_service.get_selections_for_user(user)

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
        }


class ShowBookDetailPageUsecase(Usecase):
    """書籍詳細画面を表示する。"""

    def __init__(
        self, book_service: BookDomainService, review_service: ReviewDomainService
    ):
        self.book_service = book_service
        self.review_service = review_service

    def run(self, book_id, user):
        book = self.book_service.find_book_by_id(book_id)

        # 閲覧数のカウントアップ
        book.views += 1
        book.save()

        latest_review = self.review_service.get_latest_review_for_user(book, user)
        avg_rating = book.get_avg_rating()
        reviews = book.get_reviews()
        book_on_shelf = self.book_service.is_book_on_shelf(book, user)
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


class AddBookToShelfUsecase(Usecase):
    """本棚に本を追加する。"""

    def __init__(
        self,
        book_service: BookDomainService,
        reading_record_service: RecordDomainService,
    ):
        self.book_service = book_service
        self.reading_record_service = reading_record_service

    def run(self, book_id, user):
        book = self.book_service.find_book_by_id(book_id)
        bookshelf: Bookshelf = self.book_service.get_or_create_bookshelf(user)
        bookshelf.books.add(book)

        # 登録時にRecordを作成する
        record = self.reading_record_service.get_or_create_record(user, book)
        print(record)

        return {}


class RemoveBookFromShelfUsecase(Usecase):
    """本棚から本を削除する。"""

    def __init__(self, book_service: BookDomainService):
        self.book_service = book_service

    def run(self, book_id, user):
        book = self.book_service.find_book_by_id(book_id)

        # TODO recordを削除する

        bookshelf: Bookshelf = self.book_service.get_or_create_bookshelf(user)
        bookshelf.books.remove(book)

        return {}

class CreateBookSelectionUsecase(Usecase):
    def __init__(self, book_selection_service: BookSelectionDomainService):
        self.book_selection_service = book_selection_service
    
    def run(self, body, user):
        form = BookSelectionForm(body)
        if form.is_valid():
            selection = form.save(commit=False)
            selection.user = user
            selection.save()
            form.save_m2m()
        else:
            raise ApplicationException(form.errors)

class DetailBookSelectionUsecase(Usecase):
    def __init__(self, book_selection_service: BookSelectionDomainService):
        self.book_selection_service = book_selection_service
    
    def run(self, selection_id):
        selection = self.book_selection_service.get_selection_by_id(selection_id)
        return {"selection": selection}
