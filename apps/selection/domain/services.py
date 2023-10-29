from apps.book.domain.repositories import BookSelectionRepository
from apps.selection.forms import BookSelectionForm
from apps.selection.models import BookSelection
from config.exceptions import ApplicationException, NotOwnerError
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

User = get_user_model()

class BookSelectionDomainService(object):
    def __init__(self, book_selection_repo: BookSelectionRepository):
        self.book_selection_repo = book_selection_repo
    
    @classmethod
    def initialize(cls):
        book_selection_repo = BookSelectionRepository()
        return cls(book_selection_repo)
    
    def ensure_user_is_owner(self, selection: BookSelection, user: User):
        if selection.user != user:
            raise NotOwnerError()

    def get_or_create(self, user) -> BookSelection:
        return self.book_selection_repo.fetch_or_create(user)

    def get_selections_for_user(self, user):
        return self.book_selection_repo.fetch_selections_for_user(user)

    def get_selection_by_id(self, selection_id: int) -> BookSelection:
        try:
            return BookSelection.objects.get(id=selection_id)
        except BookSelection.DoesNotExist:
            raise ApplicationException("セレクションが存在しません。")
    
    def get_latest_selection_list(self):
        return self.book_selection_repo.fetch_latest_selection_list()

    def save_selection(self, selection_data, user, existing_selection=None):
        form = BookSelectionForm(selection_data, instance=existing_selection)
        if form.is_valid():
            selection = form.save(commit=False)
            selection.user = user
            selection.save()
            form.save_m2m()
            return selection.id
        else:
            raise ApplicationException(form.errors)
