import logging

from datetime import datetime

from django.db.models import Q, Avg

from apps.book.models import Author, Book, Bookshelf
from apps.selection.models import BookSelection

logger = logging.getLogger("app_logger")


class BookRepository(object):
    @staticmethod
    def find_random_book():
        return Book.objects.all().filter(is_sensitive=False).order_by("?").first()

    @classmethod
    def fetch_books(cls, limit=20):
        return Book.objects.all().order_by("-created_at")[:limit]

    @classmethod
    def fetch_most_viewed_books(cls, limit=20):
        return Book.objects.all().filter(is_clean=False).order_by("-views")[:limit]

    @staticmethod
    def search_by_title(query):
        return list(Book.objects.filter(title__icontains=query).order_by("isbn_10").order_by("-isbn_13").order_by("-views"))

    @staticmethod
    def find_by_id(book_id):
        return Book.objects.get(id=book_id)
    
    @staticmethod
    def get_reviews_of(book):
        return book.review_set.all().order_by("-created_at")
    
    @staticmethod
    def get_avg_rating_of(book):
        """書籍の平均評価を取得する。"""
        avg_rating = book.review_set.aggregate(avg_rating=Avg("rating"))["avg_rating"]
        return round(avg_rating, 2) if avg_rating is not None else None

    @staticmethod
    def get_or_create(book_data):
        # TODO repositoryにこの責任量は多すぎるのでService層に移動する
        # 作者処理
        author_objects = []
        for author_name in book_data.get("authors", []):
            author, _ = AuthorRepository.get_or_create_by_name(author_name)
            author_objects.append(author)

        book_data.pop("authors")

        try:
            published_date = BookRepository._convert_to_date_format(
                book_data["published_date"]
            )
        except Exception as e:
            print(e)
            published_date = None

        # TODO ちょっと汚い
        try:
            book, created = Book.objects.get_or_create(
                title=book_data["title"],
                description=book_data["description"],
                thumbnail=book_data["thumbnail"],
                isbn_10=book_data["isbn_10"],
                isbn_13=book_data["isbn_13"],
                other=book_data["other"],
                published_date=published_date,
                publisher=book_data["publisher"],
                views=book_data["views"],
                is_sensitive=book_data["is_sensitive"],
            )
        except Exception as e:
            print(e)
            book = Book.objects.filter(
                Q(isbn_10=book_data["isbn_10"]) | Q(isbn_13=book_data["isbn_13"])
            ).first()

        if book:
            for author in author_objects:
                book.authors.add(author)
        else:
            return None

        for author in author_objects:
            book.authors.add(author)

        return book

    # TODO リファクタリング予定 ここじゃないよね
    @staticmethod
    def _convert_to_date_format(date_str):
        """YYYY-MM-DD形式に変換。変換不可の場合はNoneを返す。"""
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            print(date_str + "は変換できませんでした。")
            return None


class BookshelfRepository:
    @staticmethod
    def get_or_create(user):
        bookshelf, created = Bookshelf.objects.get_or_create(user=user)
        return bookshelf

    @staticmethod
    def has_book_for_user(book, user):
        return Bookshelf.objects.filter(user=user, books=book).exists()
    
    @staticmethod
    def count_books_on_shelf(book):
        return Bookshelf.objects.filter(books__id=book.id).count()


class BookSelectionRepository(object):
    @classmethod
    def fetch_or_create(user):
        book_selection, created = BookSelection.objects.get_or_create(user=user)
        return book_selection

    @classmethod
    def fetch_selections_for_user(cls, user):
        return BookSelection.objects.all().filter(user=user)
    
    @classmethod
    def fetch_selection_by_id(cls, selection_id):
        return BookSelection.objects.get(id=selection_id)
    
    @classmethod
    def fetch_latest_selection_list(cls, limit=6):
        return cls._fetch_selection().order_by("-created_at")[:limit]
    
    @classmethod
    def _fetch_selection(cls, is_public=True):
        return BookSelection.objects.all().filter(is_public=is_public)


class AuthorRepository(object):
    @staticmethod
    def get_or_create_by_name(name):
        return Author.objects.get_or_create(name=name)

