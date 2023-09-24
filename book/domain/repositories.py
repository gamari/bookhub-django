from datetime import datetime
import requests
from book.models import Author, Book, Bookshelf
from django.db.models import Q

class AuthorRepository:
    @staticmethod
    def get_or_create_by_name(name):
        return Author.objects.get_or_create(name=name)


class BookRepository:
    @staticmethod
    def search_by_title(query):
        return list(Book.objects.filter(title__icontains=query))

    @staticmethod
    def find_by_id(book_id):
        return Book.objects.get(id=book_id)

    @staticmethod
    def get_or_create(book_data):
        author_objects = []
        for author_name in book_data.get("authors", []):
            print(author_name)
            author, _ = AuthorRepository.get_or_create_by_name(author_name)
            author_objects.append(author)

        book_data.pop("authors")

        try:
            published_date = BookRepository._convert_to_date_format(book_data["published_date"])

            book, created = Book.objects.get_or_create(
                title=book_data["title"],
                description=book_data["description"],
                thumbnail=book_data["thumbnail"],
                isbn_10=book_data["isbn_10"],
                isbn_13=book_data["isbn_13"],
                published_date=published_date
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
    
    # TODO リファクタリング予定
    @staticmethod
    def _convert_to_date_format(date_str):
        """YYYY-MM-DD形式に変換。変換不可の場合はNoneを返す。"""
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except Exception:
            return None


class BookshelfRepository:
    @staticmethod
    def has_book_for_user(book, user):
        return Bookshelf.objects.filter(user=user, books=book).exists()


