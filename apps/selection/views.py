from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from config.exceptions import ApplicationException
from apps.book.application.usecases import CreateBookSelectionUsecase, DetailBookSelectionUsecase
from apps.book.domain.repositories import BookSelectionRepository
from apps.book.domain.services import BookSelectionDomainService
from apps.book.forms import BookSelectionForm
from apps.selection.models import BookSelection
from config.utils import create_ogp_image


@login_required
def create_selection(request):
    error_message = None

    if request.method == "POST":
        try:
            selection_service = BookSelectionDomainService(BookSelectionRepository())
            usecase = CreateBookSelectionUsecase(selection_service)
            selection_id = usecase.execute(request.POST, request.user)

            return redirect("selection_detail", selection_id=selection_id)
        except ApplicationException as e:
            error_message = e.message

    form = BookSelectionForm(user=request.user)

    return render(
        request,
        "pages/create_selection.html",
        {
            "form": form,
            "error_message": error_message,
        },
    )


def selection_detail(request, selection_id):
    usecase = DetailBookSelectionUsecase(
        BookSelectionDomainService(BookSelectionRepository())
    )

    context = usecase.execute(selection_id)

    return render(
        request,
        "pages/selection_detail.html",
        context
    )


@login_required
def delete_selection(request, selection_id):
    selection = BookSelection.objects.get(id=selection_id)
    selection.delete()
    return redirect("mypage")


def generate_ogp(request, selection_id):
    selection = BookSelection.objects.get(id=selection_id)
    book_covers = [book.cover_image.path for book in selection.books.all()[:3]]  # 最初の3つの書籍

    image_path = create_ogp_image(selection.title, book_covers)

    with open(image_path, 'rb') as img:
        return HttpResponse(img.read(), content_type="image/jpeg")