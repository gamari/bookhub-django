from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from apps.book.forms import BookForm

from apps.book.models import Book
from apps.contact.models import Contact

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

# お問い合わせ一覧
@user_passes_test(lambda u: u.is_superuser)
def management_contacts(request):
    contacts = Contact.objects.all().order_by("-created_at")[:10]

    context = {
        "contacts": contacts,
    }
    return render(request, "pages/manage-contacts.html", context)


# お知らせ機能