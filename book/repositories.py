import requests
from book.models import Book, Bookshelf


class BookRepository:
    @staticmethod
    def search_by_title(query):
        return list(Book.objects.filter(title__icontains=query))

    @staticmethod
    def find_by_id(book_id):
        return Book.objects.get(id=book_id)
    
    @staticmethod
    def get_or_create(book_data):
        book, created = Book.objects.get_or_create(
            title=book_data["title"],
            description=book_data["description"],
            thumbnail=book_data["thumbnail"],
            isbn_10=book_data["isbn_10"],
            isbn_13=book_data["isbn_13"]
        )
        return book

class BookshelfRepository:
    @staticmethod
    def has_book_for_user(book, user):
        return Bookshelf.objects.filter(user=user, books=book).exists()