import requests
from book.models import Author, Book, Bookshelf


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

        book, created = Book.objects.get_or_create(
            title=book_data["title"],
            description=book_data["description"],
            thumbnail=book_data["thumbnail"],
            isbn_10=book_data["isbn_10"],
            isbn_13=book_data["isbn_13"],
        )

        for author in author_objects:
            book.authors.add(author)

        return book


class BookshelfRepository:
    @staticmethod
    def has_book_for_user(book, user):
        return Bookshelf.objects.filter(user=user, books=book).exists()


class AuthorRepository:
    @staticmethod
    def get_or_create_by_name(name):
        return Author.objects.get_or_create(name=name)
