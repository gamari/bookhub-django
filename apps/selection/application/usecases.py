from apps.selection.domain.services import BookSelectionDomainService
from apps.selection.models import BookSelectionLike
from config.application.usecases import Usecase



class CreateBookSelectionUsecase(Usecase):
    def __init__(self, book_selection_service: BookSelectionDomainService):
        self.book_selection_service = book_selection_service
    
    @classmethod
    def build(cls):
        book_selection_service = BookSelectionDomainService.initialize()
        return cls(book_selection_service)

    def run(self, body, user):
        return self.book_selection_service.save_selection(body, user)

class EditBookSelectionUsecase(Usecase):
    def __init__(self, book_selection_service: BookSelectionDomainService):
        self.book_selection_service = book_selection_service
    
    @classmethod
    def build(cls):
        book_selection_service = BookSelectionDomainService.initialize()
        return cls(book_selection_service)


    def run(self, body, user, selection_id):
        existing_selection = self.book_selection_service.get_selection_by_id(selection_id)
        self.book_selection_service.ensure_user_is_owner(existing_selection, user)
        return self.book_selection_service.save_selection(body, user, existing_selection)


class DetailBookSelectionUsecase(Usecase):
    def __init__(self, book_selection_service: BookSelectionDomainService):
        self.book_selection_service = book_selection_service
    
    @classmethod
    def build(cls):
        book_selection_service = BookSelectionDomainService.initialize()
        return cls(book_selection_service)

    def run(self, selection_id, user):
        selection = self.book_selection_service.get_selection_by_id(selection_id)
        if user.is_authenticated:
            is_liked = BookSelectionLike.objects.filter(user=user, selection=selection).exists()
        else:
            is_liked = False
        return {"selection": selection, "is_liked": is_liked }

# TODO
# class LikeSelectionUsecase(Usecase):
#     def __init__(self, book_selection_service: BookSelectionDomainService):
#         self.book_selection_service = book_selection_service

#     def run(self, selection_id, user):
#         selection = self.book_selection_service.get_selection_by_id(selection_id)
#         return self.book_selection_service.like_selection(selection, user)
