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

def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    logger.debug(note)

    if note.author != request.user:
        return redirect("note_detail", note_id=note_id)
    
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.save()
            return redirect("note_detail", note_id=note_id)
        else:
            logger.debug(form.errors)
    else:
        form = NoteForm(instance=note)

    context = {
        "note": note,
        "form": form,
        "errors": form.errors,
    }

    return render(request, "pages/note/edit_note.html", context)

def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    
    logger.debug(note)
    logger.debug(note_id)
    logger.debug(request.method)

    if note.author != request.user:
        return redirect("reading_record", book_id=note.book.id)

    if request.method == "POST":
        note.delete()
        return redirect("reading_record", book_id=note.book.id)

    return redirect("reading_record", book_id=note.book.id)


def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    context = {
        "note": note,
    }

    return render(request, "pages/note/detail.html", context)