from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from config.exceptions import ApplicationException
from apps.selection.application.usecases import (
    CreateBookSelectionUsecase,
    EditBookSelectionUsecase,
)
from apps.selection.application.usecases import DetailBookSelectionUsecase
from apps.book.domain.repositories import BookSelectionRepository
from apps.selection.application.usecases import BookSelectionDomainService
from apps.book.forms import BookSelectionForm
from apps.selection.models import BookSelection
from config.utils import create_ogp_image


class CreateSelectionView(View):
    template_name = "pages/create_selection.html"

    def get(self, request, *args, **kwargs):
        return self.render_create_selection_page(user=request.user)

    def post(self, request, *args, **kwargs):
        service = self.get_book_selection_service()
        usecase = CreateBookSelectionUsecase(service)
        try:
            selection_id = usecase.execute(request.POST, request.user)
            return redirect("selection_detail", selection_id=selection_id)
        except ApplicationException as e:
            return self.render_error(e.message, user=request.user)

    def render_create_selection_page(self, user):
        form = BookSelectionForm(user=user)
        return render(
            self.request,
            self.template_name,
            {
                "form": form,
            }
        )

    def render_error(self, message, user):
        form = BookSelectionForm(user=user)
        return render(
            self.request,
            self.template_name,
            {
                "form": form,
                "error_message": message,
            }
        )

    @staticmethod
    def get_book_selection_service():
        return BookSelectionDomainService(BookSelectionRepository())


class EditSelectionView(View):
    template_name = "pages/edit_selection.html"

    def get(self, request, *args, **kwargs):
        return self.render_edit_selection_page(
            kwargs.get("selection_id"), user=request.user
        )

    def post(self, request, *args, **kwargs):
        service = self.get_book_selection_service()
        usecase = EditBookSelectionUsecase(service)
        try:
            usecase.execute(request.POST, request.user, kwargs.get("selection_id"))
            return redirect("selection_detail", selection_id=kwargs.get("selection_id"))
        except ApplicationException as e:
            return self.render_error(
                e.message, kwargs.get("selection_id"), user=request.user
            )

    def render_edit_selection_page(self, selection_id, user):
        selection = get_object_or_404(BookSelection, id=selection_id)
        form = BookSelectionForm(instance=selection, user=user)
        return render(
            self.request, self.template_name, {"form": form, "selection": selection}
        )

    def render_error(self, message, selection_id, user):
        selection = get_object_or_404(BookSelection, id=selection_id)
        form = BookSelectionForm(instance=selection, user=user)
        return render(
            self.request,
            self.template_name,
            {
                "form": form,
                "selection": selection,
                "error_message": message,
            },
        )

    @staticmethod
    def get_book_selection_service():
        return BookSelectionDomainService(BookSelectionRepository())


def selection_detail(request, selection_id):
    usecase = DetailBookSelectionUsecase(
        BookSelectionDomainService(BookSelectionRepository())
    )

    context = usecase.execute(selection_id)

    return render(request, "pages/selection_detail.html", context)


@login_required
def delete_selection(request, selection_id):
    selection = BookSelection.objects.get(id=selection_id)
    selection.delete()
    return redirect("mypage")


# TODO OGPを実装する（未完成）
def generate_ogp(request, selection_id):
    selection = BookSelection.objects.get(id=selection_id)
    book_covers = [book.thumbnail for book in selection.books.all()[:3]]

    # image_path = create_ogp_image(selection.title, book_covers)
    image_path = create_ogp_image(selection.title)

    with open(image_path, "rb") as img:
        return HttpResponse(img.read(), content_type="image/jpeg")
