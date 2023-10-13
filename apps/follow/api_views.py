from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from apps.follow.application.usecases import FollowAccountUsecase, UnfollowAccountUsecase
from apps.follow.domain.services import FollowService
from authentication.domain.repositories import AccountRepository
from authentication.domain.services import AccountDomainService

@method_decorator(csrf_exempt, name='dispatch')
@login_required
def follow_api(request, id):
    try:
        print(id)
        account_service = AccountDomainService(AccountRepository())
        follow_service = FollowService()

        usecase = FollowAccountUsecase(
            account_service,
            follow_service
        )

        context = usecase.execute(request.user, id)

        return JsonResponse(context)
    except Exception as e:
        print(e)
        return JsonResponse({"error": "エラーが発生しました。"}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
@login_required
def unfollow_api(request, id):
    try:
        account_service = AccountDomainService(AccountRepository())
        follow_service = FollowService()

        usecase = UnfollowAccountUsecase(
            account_service,
            follow_service
        )

        context = usecase.execute(request.user, id)

        return JsonResponse(context)
    except Exception as e:
        print(e)
        return JsonResponse({"error": "エラーが発生しました。"}, status=500)