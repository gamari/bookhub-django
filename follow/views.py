from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from authentication.models import Account
from follow.domain.services import FollowService


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
