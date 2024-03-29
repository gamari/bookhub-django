from django.shortcuts import  render

from authentication.domain.repositories import AccountRepository
from authentication.domain.services import AccountDomainService

from apps.follow.application.usecases import GetFollowerUsecase, GetFollowingsUsecase


def show_follower_page(request, id):
    account_service = AccountDomainService(AccountRepository())
    usecase = GetFollowerUsecase(account_service)
    context = usecase.execute(id)

    return render(request, "pages/follower_page.html", context)


def show_following_page(request, id):
    account_service = AccountDomainService(AccountRepository())
    usecase = GetFollowingsUsecase(account_service)
    context = usecase.execute(id)

    return render(request, "pages/following_page.html", context)

