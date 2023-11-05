import logging

from django.shortcuts import get_object_or_404, redirect, render

from apps.book.models import Book
from apps.note.forms import NoteForm
from apps.note.models import Note

logger = logging.getLogger("app_logger")


def note_of_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    logger.debug(book)

    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.book = book
            note.author = request.user
            note.save()
            return render(request, "pages/note/detail.html", {"book": book, "note": note})
        else:
            logger.debug(form.errors)
    else:
        form = NoteForm()

    context = {
        "book": book,
        "form": form,
        "errors": form.errors,
    }

    return render(request, "pages/note/create_note_of_book.html", context)

def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    context = {
        "note": note,
    }

    return render(request, "pages/note/detail.html", context)