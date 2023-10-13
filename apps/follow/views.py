from django.shortcuts import  render

from authentication.domain.repositories import AccountRepository
from authentication.domain.services import AccountDomainService

from apps.follow.application.usecases import ShowFollowerPage


def show_follower_page(request, id):
    account_service = AccountDomainService(AccountRepository())
    usecase = ShowFollowerPage(account_service)
    context = usecase.execute(id)

    return render(request, "pages/follower_page.html", context)


