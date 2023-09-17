# your_app/management/commands/fetch_books.py
import requests
from django.core.management.base import BaseCommand

from book.models import Author, Book


class Command(BaseCommand):
    help = "書籍を登録します。"

    def handle(self, *args, **options):
        url = "https://www.googleapis.com/books/v1/volumes?q=Java"

        response = requests.get(url)
        data = response.json()

        for item in data["items"]:
            volume_info = item["volumeInfo"]

            if "industryIdentifiers" not in volume_info:
                continue

            isbn_10 = isbn_13 = None
            for identifier in volume_info["industryIdentifiers"]:
                if identifier["type"] == "ISBN_10":
                    isbn_10 = identifier["identifier"]
                elif identifier["type"] == "ISBN_13":
                    isbn_13 = identifier["identifier"]

            if not isbn_10 and not isbn_13:
                continue

            authors_objs = []
            for author_name in volume_info.get("authors", []):
                author_obj, created = Author.objects.get_or_create(name=author_name)
                authors_objs.append(author_obj)
            
            # TODO 出版日を入れる

            book, created = Book.objects.update_or_create(
                title=volume_info["title"],
                defaults={
                    "isbn_10": isbn_10,
                    "isbn_13": isbn_13,
                    "description": volume_info.get("description"),
                    "thumbnail": volume_info.get("imageLinks", {}).get("thumbnail"),
                },
            )
            book.authors.set(authors_objs)

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully added/updated book "{volume_info["title"]}"'
                )
            )
