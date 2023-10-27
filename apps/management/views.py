from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from apps.book.forms import BookForm

from apps.book.models import Book
from apps.contact.models import Contact
from apps.management.forms import NoticeForm
from apps.management.models import Notice
from apps.search.models import SearchHistory

@user_passes_test(lambda u: u.is_superuser)
def management_notices(request):
    """お知らせ一覧画面。"""
    notices = Notice.objects.all().order_by("-created_at")

    context = {
        "notices": notices,
    }
    return render(request, "pages/manage-notices.html", context)

# お知らせ作成
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

# お知らせの編集
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



@user_passes_test(lambda u: u.is_superuser)
def management_dashboard(request):
    context = {}
    return render(request, "pages/manage-dashboard.html", context)

@user_passes_test(lambda u: u.is_superuser)
def management_books(request):
    books = Book.objects.all().filter(is_clean=False).order_by("-views")[:10]
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