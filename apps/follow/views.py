from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from authentication.domain.repositories import AccountRepository
from authentication.domain.services import AccountDomainService
from authentication.models import Account

from apps.follow.application.usecases import ShowFollowerPage
from apps.follow.domain.services import FollowService


def show_follower_page(request, id):
    account_service = AccountDomainService(AccountRepository())
    usecase = ShowFollowerPage(account_service)
    context = usecase.execute(id)

    return render(request, "pages/follower_page.html", context)


# TODO toggle followとかのほうが良いかも
@login_required
def follow_account(request, id):
    target_account = get_object_or_404(Account, id=id)

    if request.user == target_account:
        return HttpResponse("自分自身はフォローできません。", status=400)

    service = FollowService()

    followed = service.follow(request.user, target_account)

    if followed:
        return redirect("user_detail", str(target_account.username))
    else:
        return HttpResponse("フォローに失敗しました。", status=400)


@login_required
def unfollow_account(request, id):
    target_account = get_object_or_404(Account, id=id)

    if request.user == target_account:
        return HttpResponse("自分自身はフォロー解除できません。", status=400)

    service = FollowService()

    followed = service.unfollow(request.user, target_account)

    if followed:
        return redirect("user_detail", str(target_account.username))
    else:
        return HttpResponse("フォロー解除に失敗しました。", status=400)


# TODO apiを作成する
