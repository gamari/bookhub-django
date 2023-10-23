from apps.book.domain.repositories import BookRepository, BookshelfRepository
from apps.book.models import Bookshelf


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

    def find_book_by_id(self, book_id):
        return self.book_repository.find_by_id(book_id)

    def is_book_on_shelf(self, book, user):
        if not user.is_authenticated:
            return False
        return self.bookshelf_repository.has_book_for_user(book, user)

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


class BookshelfDomainService(object):
    def __init__(self, bookshelf_repo: BookshelfRepository):
        self.bookshelf_repo = bookshelf_repo

    def get_or_create(self, user) -> Bookshelf:
        return self.bookshelf_repo.get_or_create(user)

    @classmethod
    def initialize(cls):
        bookshelf_repo = BookshelfRepository()
        return cls(bookshelf_repo)