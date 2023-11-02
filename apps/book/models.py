import uuid, logging

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Prefetch, Max


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

class Tag(models.Model):
    name = models.CharField("タグ名", max_length=255, unique=True)
    created_at = models.DateTimeField("作成日", auto_now_add=True)

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
    """
    書籍モデル
    関係ある場所
    - ReadingMemo, Review, BookshelfBook
    """

    id = models.AutoField(primary_key=True)
    isbn_10 = models.CharField(max_length=10, unique=True, null=True, blank=True)
    isbn_13 = models.CharField(max_length=13, unique=True, null=True, blank=True)
    other = models.CharField(verbose_name="ISBN意外のキー", max_length=255, null=True, blank=True, unique=True)
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
    is_sensitive = models.BooleanField("センシティブな内容", default=False)
    is_clean = models.BooleanField("整備されたデータ判定", default=False)
    amazon_url = models.URLField("Amazonの購入URL", null=True, blank=True)
    tags = models.ManyToManyField(Tag, through="BookTag", verbose_name="タグ", blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.title}"
    
    def save(self, *args, **kwargs):
        if self.thumbnail and self.thumbnail.startswith("http:"):
            # Mixed Content対策
            self.thumbnail = self.thumbnail.replace("http:", "https:")
        super(Book, self).save(*args, **kwargs)


class Bookshelf(models.Model):
    """本棚。"""

    id: uuid.UUID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, through="BookshelfBook")

    def __str__(self) -> str:
        return f"[{self.user.username}]の本棚"

    def add_book(self, book: Book):
        logger.debug(f"{book}")
        if not self.books.filter(id=book.id).exists():
            self.books.add(book)
    
    def add_books(self, books):
        logger.debug(f"{self}に書籍を追加します。")
        for book in books:
            self.add_book(book)

    def remove_book(self, book: Book):
        self.books.remove(book)

    def get_books(self):
        return self.books.all().prefetch_related()

    def get_books_with_reading_records(self, user):
        from apps.record.models import ReadingRecord
        reading_records_ordered = ReadingRecord.objects.filter(user=user).order_by('-updated_at')
        books_with_records = self.books.all().prefetch_related(
            Prefetch(
                "readingrecord_set",
                queryset=reading_records_ordered,
                to_attr="user_reading_records"
            )
        )

        books_with_records_list = list(books_with_records.distinct())

        books_with_records_list.sort(key=lambda b: b.user_reading_records[0].updated_at if b.user_reading_records else None, reverse=True)

        return books_with_records_list

    def contains(self, book: Book):
        return self.books.filter(id=book.id).exists()


### 以下中間テーブル


class BookshelfBook(models.Model):
    """BookshelfとBookの中間テーブル"""

    bookshelf = models.ForeignKey(Bookshelf, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("bookshelf", "book")


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

class BookTag(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="書籍")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="タグ")
    created_at = models.DateTimeField("タグ付け日", auto_now_add=True)

    class Meta:
        unique_together = ('book', 'tag')
