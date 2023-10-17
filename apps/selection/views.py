from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from config.exceptions import ApplicationException
from apps.book.application.usecases import CreateBookSelectionUsecase, DetailBookSelectionUsecase
from apps.book.domain.repositories import BookSelectionRepository
from apps.book.domain.services import BookSelectionDomainService
from apps.book.forms import BookSelectionForm
from apps.selection.models import BookSelection


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
