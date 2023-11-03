from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from apps.book.application.usecases import (
    AddBookToShelfUsecase,
    ShowBookDetailPageUsecase,
    ShowHomePageUsecase,
    ShowMyPageUsecase,
    RemoveBookFromShelfUsecase,
)
from apps.book.models import Bookshelf


def home(request):
    usecase = ShowHomePageUsecase.build()
    context = usecase.execute()
    
    return render(request, "pages/home.html", context)


@login_required
def mypage(request):
    usecase = ShowMyPageUsecase.build()
    context = usecase.execute(request.user)

    return render(request, "pages/mypage.html", context)


def book_detail_page(request, book_id):
    usecase = ShowBookDetailPageUsecase.build()
    context = usecase.execute(book_id, request.user)

    return render(request, "pages/book_detail.html", context)


def bookshelf_list_page(request, bookshelf_id):
    bookshelf = Bookshelf.objects.get(id=bookshelf_id)
    return render(request, "bookshelf_list.html", {"bookshelf": bookshelf})


@login_required
def add_book_to_shelf(request, book_id):
    usecase = AddBookToShelfUsecase.build()
    usecase.execute(book_id, request.user)

    return redirect("book_detail", book_id=book_id)


@login_required
def remove_book_from_shelf(request, book_id):
    usecase = RemoveBookFromShelfUsecase.build()
    usecase.execute(book_id, request.user)

    return redirect("book_detail", book_id=book_id)


