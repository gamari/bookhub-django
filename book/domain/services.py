from typing import Any


# 書籍ドメイン
class BookDomainService:
    def __init__(self, book_repository, bookshelf_repository):
        self.book_repository = book_repository
        self.bookshelf_repository = bookshelf_repository

    def find_book_by_id(self, book_id):
        """書籍IDから書籍を取得する。"""
        return self.book_repository.find_by_id(book_id)

    def is_book_on_shelf(self, book, user):
        """書籍が本棚に含まれているかどうかを判定する。"""
        if not user.is_authenticated:
            return False
        return self.bookshelf_repository.has_book_for_user(book, user)

    def get_or_create_books(self, books_data):
        """書籍一覧を取得または作成する。"""
        books = []
        for book_data in books_data:
            book = self.book_repository.get_or_create(book_data)
            if book:
                books.append(book)
        return books
    
    def get_or_create_bookshelf(self, user):
        """本棚を取得または作成する。"""
        return self.bookshelf_repository.get_or_create(user)
