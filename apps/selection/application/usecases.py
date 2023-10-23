from apps.selection.domain.services import BookSelectionDomainService
from config.application.usecases import Usecase



class CreateBookSelectionUsecase(Usecase):
    def __init__(self, book_selection_service: BookSelectionDomainService):
        self.book_selection_service = book_selection_service

    def run(self, body, user):
        return self.book_selection_service.save_selection(body, user)

class EditBookSelectionUsecase(Usecase):
    def __init__(self, book_selection_service: BookSelectionDomainService):
        self.book_selection_service = book_selection_service

    def run(self, body, user, selection_id):
        existing_selection = self.book_selection_service.get_selection_by_id(selection_id)
        self.book_selection_service.ensure_user_is_owner(existing_selection, user)
        return self.book_selection_service.save_selection(body, user, existing_selection)


class DetailBookSelectionUsecase(Usecase):
    def __init__(self, book_selection_service: BookSelectionDomainService):
        self.book_selection_service = book_selection_service

    def run(self, selection_id):
        selection = self.book_selection_service.get_selection_by_id(selection_id)
        return {"selection": selection}
