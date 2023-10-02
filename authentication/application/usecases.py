from django.shortcuts import get_object_or_404
from book.models import Bookshelf
from config.application.usecases import Usecase
from review.views import Account


class UserDetailShowUsecase(Usecase):
    def __init__(self, username, bookshelf_repository):
        self.username = username
        self.bookshelf_repository = bookshelf_repository

    def execute(self):
        user = get_object_or_404(Account, username=self.username)

        bookshelf: Bookshelf = self.bookshelf_repository.get_or_create(user=user)
        books = bookshelf.get_books()

        return {"user": user, "books": books, "bookshelf": bookshelf}
