import logging

from apps.book.domain.repositories import BookRepository, BookshelfRepository
from apps.book.models import Bookshelf

logger = logging.getLogger("app_logger")


class BookDomainService(object):
    def __init__(
        self, book_repository: BookRepository, bookshelf_repository: BookshelfRepository
    ):
        self.book_repository = book_repository
        self.bookshelf_repository = bookshelf_repository
    
    @classmethod
    def initialize(cls):
        book_repository = BookRepository()
        bookshelf_repository = BookshelfRepository()
        return cls(book_repository, bookshelf_repository)

    def get_book_by_id(self, book_id):
        return self.book_repository.find_by_id(book_id)
    
    def get_random_book(self):
        return self.book_repository.find_random_book()

    def is_book_on_shelf(self, book, user):
        if not user.is_authenticated:
            return False
        return self.bookshelf_repository.has_book_for_user(book, user)
    
    def count_books_on_shelf(self, book):
        return self.bookshelf_repository.count_books_on_shelf(book)
    

    def get_or_create_books(self, books_data):
        books = []
        for book_data in books_data:
            book = self.book_repository.get_or_create(book_data)
            if book:
                books.append(book)
        return books

    # TODO 削除予定
    def get_or_create_bookshelf(self, user):
        return self.bookshelf_repository.get_or_create(user)
    
    def get_reviews_of_book(self, book, user=None):
        """本に対するレビューを取得する。"""
        reviews = self.book_repository.get_reviews_of(book)

        if user and user.is_authenticated:
            for review in reviews:
                review.is_liked = review.is_liked_by(user)

        return reviews
    
    def increment_views_of_book(self, book):
        book.views += 1
        book.save()
    
    def get_avg_rating_of_book(self, book):
        """書籍の平均評価を取得する。"""
        avg_rating = self.book_repository.get_avg_rating_of(book)
        return round(avg_rating, 2) if avg_rating is not None else None


class BookshelfDomainService(object):
    def __init__(self, bookshelf_repo: BookshelfRepository):
        self.bookshelf_repo = bookshelf_repo

    def get_or_create(self, user) -> Bookshelf:
        return self.bookshelf_repo.get_or_create(user)
    
    def add_books(self, books, user):
        bookshelf = self.bookshelf_repo.get_or_create(user)
        bookshelf.add_books(books)
        bookshelf.save()

    @classmethod
    def initialize(cls):
        bookshelf_repo = BookshelfRepository()
        return cls(bookshelf_repo)