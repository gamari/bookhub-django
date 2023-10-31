import logging

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count

from apps.book.domain.repositories import BookRepository
from apps.book.forms import BookForm

from apps.book.models import Book, BookAuthor, BookGenre, BookshelfBook
from apps.contact.models import Contact
from apps.management.forms import NoticeForm
from apps.management.models import Notice
from apps.record.models import ReadingMemo
from apps.review.models import Review
from apps.search.models import SearchHistory
from apps.selection.models import SelectionBookRelation
from authentication.forms import AccountUpdateForm
from authentication.models import Account

logger = logging.getLogger("app_logger")

@user_passes_test(lambda u: u.is_superuser)
def management_notices(request):
    """お知らせ一覧画面。"""
    notices = Notice.objects.all().order_by("-created_at")

    context = {
        "notices": notices,
    }
    return render(request, "pages/manage-notices.html", context)

@user_passes_test(lambda u: u.is_superuser)
def management_notice_create(request):
    """お知らせ作成画面。"""
    if request.method == "POST":
        form = NoticeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('management_notices')
    else:
        form = NoticeForm()
    context = {
        "form": form,
    }
    return render(request, "pages/manage-notice-create.html", context)

@user_passes_test(lambda u: u.is_superuser)
def management_notice_edit(request, notice_id):
    """お知らせ編集画面。"""
    notice = Notice.objects.get(id=notice_id)
    if request.method == "POST":
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            return redirect('management_notices')
    else:
        form = NoticeForm(instance=notice)    
    
    context = {
        "form": form,
    }
    
    return render(request, "pages/manage-notice-edit.html", context)

# お知らせの削除
@user_passes_test(lambda u: u.is_superuser)
def management_notice_delete(request, notice_id):
    if request.user.is_superuser:
        notice = Notice.objects.get(id=notice_id)
        notice.delete()
        logger.info("削除しました")
        return redirect('management_notices')

    logger.info("削除できません")
    return redirect('management_notices')



@user_passes_test(lambda u: u.is_superuser)
def management_dashboard(request):
    context = {}
    return render(request, "pages/manage-dashboard.html", context)

@user_passes_test(lambda u: u.is_superuser)
def management_books(request):
    repository = BookRepository()
    books = repository.fetch_most_viewed_books()
    context = {
        "books": books,
    }
    return render(request, "pages/manage-books.html", context)



@user_passes_test(lambda u: u.is_superuser)
def management_delete_book(request, book_id):
    logger.info("削除します")
    book = Book.objects.get(id=book_id)
    book.delete()
    logger.info("削除しました")
    logger.info(book)
    return redirect('management_books')

# 重複書籍一覧
@user_passes_test(lambda u: u.is_superuser)
def management_duplicate_books(request):
    duplicated_others = (
        Book.objects.values("other")
        .annotate(count=Count("other"))
        .filter(count__gt=1, other__isnull=False)
        .values_list("other", flat=True)
    )
    
    duplicated_books = Book.objects.filter(other__in=duplicated_others).order_by("title")
    
    context = {
        "books": duplicated_books,
    }
    logger.debug(duplicated_books)

    return render(request, "pages/manage-duplicate-books.html", context)



@user_passes_test(lambda u: u.is_superuser)
def management_delete_duplicate_book(request, book_id):
    logger.info("削除します")
    book = Book.objects.get(id=book_id)
    book.delete()
    logger.info("削除しました")
    logger.info(book)
    return redirect('management_book_duplicate')

@user_passes_test(lambda u: u.is_superuser)
def management_book_edit(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('management_books')
    else:
        form = BookForm(instance=book)
    context = {
        "book": book,
        "form": form,
    }
    return render(request, "pages/manage-book-edit.html", context)

# AIユーザー一覧
@user_passes_test(lambda u: u.is_superuser)
def management_ai_users(request):
    users = Account.objects.filter(is_ai=True)
    context = {
        "users": users,
    }
    return render(request, "pages/manage-ai-users.html", context)


@user_passes_test(lambda u: u.is_superuser)
def management_ai_users_edit(request, user_id):
    user = Account.objects.get(id=user_id)

    if request.method == "POST":
        form = AccountUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('management_ai_users')
    else:
        form = AccountUpdateForm(instance=user)
    context = {
        "user": user,
        "form": form,
    }
    return render(request, "pages/manage-ai-users-edit.html", context)



# TODO マージ処理を完成させる
@user_passes_test(lambda u: u.is_superuser)
def management_book_merge(request, source_id, target_id):
    """
    source_id= 合体させる
    target_id= 大元
    """
    target_book = Book.objects.get(id=target_id)
    source_book = Book.objects.get(id=source_id)

    if target_book.id == source_book.id:
        logger.info("同じ本です")
        return redirect('management_books')


    logger.info("マージします")
    logger.info(target_book)
    logger.info(source_book)

    # 関連データの更新
    # メモ
    memos = ReadingMemo.objects.filter(book=source_book)
    for memo in memos:
        memo.book = target_book
        memo.save()

    # レビュー
    reviews = Review.objects.filter(book=source_book)
    for review in reviews:
        review.book = target_book
        review.save()
    
    # 本棚
    bookshelf_books = BookshelfBook.objects.filter(book=source_book)
    for bookshelf_book in bookshelf_books:
        bookshelf_book.book = target_book
        bookshelf_book.save()
    
    book_authors = BookAuthor.objects.filter(book=source_book)
    for book_author in book_authors:
        book_author.book = target_book
        book_author.save()
    
    book_genres = BookGenre.objects.filter(book=source_book)
    for book_genre in book_genres:
        book_genre.book = target_book
        book_genre.save()

    # セレクション
    source_selection_books = SelectionBookRelation.objects.filter(book=source_book)
    logger.info(source_selection_books)

    try:
        for selection_book in source_selection_books:
            selection_book.book = target_book
            selection_book.save()
    except:
        logger.info("失敗")

    # 本の情報の更新
    # target_book.title = source_book.title
    # target_book.description = source_book.description

    target_book.save()
    source_book.delete()
    return redirect('management_books')


@user_passes_test(lambda u: u.is_superuser)
def management_contacts(request):
    contacts = Contact.objects.all().order_by("-created_at")[:10]

    context = {
        "contacts": contacts,
    }
    return render(request, "pages/manage-contacts.html", context)

@user_passes_test(lambda u: u.is_superuser)
def management_search_history(request):
    histories = SearchHistory.objects.all().order_by("-created_at")[:50]
    context = {
        "histories": histories,
    }
    return render(request, "pages/manage-search-history.html", context)

