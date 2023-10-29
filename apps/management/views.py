from datetime import datetime
import logging 

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import user_passes_test
from apps.book.domain.repositories import BookRepository
from apps.book.forms import BookForm

from apps.book.models import Book
from apps.contact.models import Contact
from apps.management.forms import NoticeForm
from apps.management.models import Notice
from apps.record.models import ReadingMemo
from apps.search.models import SearchHistory

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

@user_passes_test(lambda u: u.is_superuser)
def management_book_merge(request, source_id, target_id):
    target_book = Book.objects.get(id=target_id)
    source_book = Book.objects.get(id=source_id)

    # 関連データの更新
    # メモ
    memos = ReadingMemo.objects.filter(book=source_book)
    for memo in memos:
        memo.book = target_book
        memo.save()

    # レビュー
    # セレクション

    # 本の情報の更新
    target_book.title = source_book.title
    target_book.description = source_book.description

    target_book.save()
    source_book.delete()


@user_passes_test(lambda u: u.is_superuser)
def management_delete_book(request, book_id):
    logger.info("削除します")
    book = Book.objects.get(id=book_id)
    book.delete()
    logger.info("削除しました")
    logger.info(book)
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


# お知らせ機能