import uuid, logging

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Avg, Prefetch

logger = logging.getLogger("app_logger")

Account = get_user_model()


class Genre(models.Model):
    """ジャンル。"""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    """著者。"""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class BookCategory(models.Model):
    """
    書籍カテゴリ。
    漫画 = comic
    小説 = novel
    ライトノベル = light_novel
    """

    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(verbose_name="表示名", max_length=255)
    description = models.TextField(verbose_name="説明", null=True, blank=True)


class Book(models.Model):
    """書籍。"""

    id = models.AutoField(primary_key=True)
    isbn_10 = models.CharField(max_length=10, unique=True, null=True, blank=True)
    isbn_13 = models.CharField(max_length=13, unique=True, null=True, blank=True)
    other = models.CharField(verbose_name="ISBN意外のキー", max_length=255, null=True, blank=True)
    title = models.CharField("書籍名", max_length=255)
    description = models.TextField("書籍説明", null=True, blank=True)
    category = models.ForeignKey(
        BookCategory,
        verbose_name="カテゴリ",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    authors = models.ManyToManyField(Author, through="BookAuthor")
    thumbnail = models.URLField("サムネイル", null=True, blank=True)
    published_date = models.DateField("出版日", null=True, blank=True)
    publisher = models.CharField("出版社", max_length=255, null=True, blank=True)
    views = models.IntegerField("閲覧数", default=0)
    genres = models.ManyToManyField(Genre, through="BookGenre")
    is_clean = models.BooleanField("整備されたデータ判定", default=False)

    def __str__(self):
        return f"{self.title}"


class Bookshelf(models.Model):
    """本棚。"""

    id: uuid.UUID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, through="BookshelfBook")

    def add_book(self, book: Book):
        self.books.add(book)

    def remove_book(self, book: Book):
        self.books.remove(book)

    def get_books(self):
        return self.books.all().prefetch_related()

    def get_books_with_reading_records(self, user):
        from apps.record.models import ReadingRecord

        books_with_records = self.books.all().prefetch_related(
            Prefetch(
                "readingrecord_set",
                queryset=ReadingRecord.objects.filter(user=user),
                to_attr="reading_record",
            )
        )

        return books_with_records

    def contains(self, book: Book):
        return self.books.filter(id=book.id).exists()


### 以下中間テーブル


class BookshelfBook(models.Model):
    """BookshelfとBookの中間テーブル"""

    bookshelf = models.ForeignKey(Bookshelf, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class BookAuthor(models.Model):
    """BookとAuthorの中間テーブル"""

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("book", "author")


class BookGenre(models.Model):
    """BookとGenreの中間テーブル"""

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("book", "genre")
