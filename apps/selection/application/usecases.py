from apps.book.domain.services import BookSelectionDomainService
from apps.book.forms import BookSelectionForm
from apps.selection.models import BookSelection
from config.application.usecases import Usecase
from config.exceptions import ApplicationException


from django.core.exceptions import PermissionDenied


class CreateBookSelectionUsecase(Usecase):
    def __init__(self, book_selection_service: BookSelectionDomainService):
        self.book_selection_service = book_selection_service

    def run(self, body, user):
        form = BookSelectionForm(body)
        if form.is_valid():
            selection = form.save(commit=False)
            selection.user = user
            selection.save()
            form.save_m2m()
            return selection.id
        else:
            raise ApplicationException(form.errors)


class EditBookSelectionUsecase(Usecase):
    def __init__(self, book_selection_service: BookSelectionDomainService):
        self.book_selection_service = book_selection_service

    def run(self, body, user, selection_id):
        try:
            existing_selection = BookSelection.objects.get(id=selection_id)

            if existing_selection.user != user:
                raise PermissionDenied(
                    "編集権限がありません。"
                )

            form = BookSelectionForm(body, instance=existing_selection)
            if form.is_valid():
                selection = form.save(commit=False)
                selection.user = user
                selection.save()
                form.save_m2m()
                return selection.id
            else:
                raise ApplicationException(form.errors)

        except BookSelection.DoesNotExist:
            raise ApplicationException("セレクションが存在しません。")


class DetailBookSelectionUsecase(Usecase):
    def __init__(self, book_selection_service: BookSelectionDomainService):
        self.book_selection_service = book_selection_service

    def run(self, selection_id):
        selection = self.book_selection_service.get_selection_by_id(selection_id)
        return {"selection": selection}
