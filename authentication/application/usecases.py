from django.shortcuts import get_object_or_404
from book.models import Bookshelf
from config.application.usecases import Usecase
from follow.domain.services import FollowService
from review.views import Account


class UserDetailShowUsecase(Usecase):
    def __init__(self, username, me, bookshelf_repository):
        self.username = username
        self.bookshelf_repository = bookshelf_repository
        self.me = me

    def execute(self):
        user = get_object_or_404(Account, username=self.username)

        bookshelf: Bookshelf = self.bookshelf_repository.get_or_create(user=user)
        books = bookshelf.get_books_with_reading_records(user)

        is_self = user == self.me

        # フォロー判定
        follow_service = FollowService()
        is_following = follow_service.is_following(self.me.id, user.id)

        following_count = follow_service.get_following_count(user.id)

        follower_count = follow_service.get_follower_count(user.id)

        return {
            "user": user,
            "books": books,
            "bookshelf": bookshelf,
            "is_self": is_self,
            "is_following": is_following,
            "following_count": following_count,
            "follower_count": follower_count,
        }
