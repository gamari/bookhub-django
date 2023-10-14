from datetime import datetime

from django.db.models import Q

from apps.book.models import Author, Book, BookSelection, Bookshelf


class AuthorRepository(object):
    @staticmethod
    def get_or_create_by_name(name):
        return Author.objects.get_or_create(name=name)


class BookRepository(object):
    @staticmethod
    def search_by_title(query):
        return list(Book.objects.filter(title__icontains=query).order_by("-views"))

    @staticmethod
    def find_by_id(book_id):
        return Book.objects.get(id=book_id)

    @staticmethod
    def get_or_create(book_data):
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
                published_date=published_date,
                publisher=book_data["publisher"],
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

class BookSelectionRepository(object):
    @staticmethod
    def get_or_create(user):
        book_selection, created = BookSelection.objects.get_or_create(user=user)
        return book_selection

    @staticmethod
    def get_selections_for_user(user):
        return BookSelection.objects.filter(user=user)
    
    @staticmethod
    def get_selection_by_id(selection_id):
        return BookSelection.objects.get(id=selection_id)