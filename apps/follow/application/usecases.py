from apps.follow.domain.services import FollowService
from authentication.domain.services import AccountDomainService
from authentication.models import Account

from config.application.usecases import Usecase


class GetFollowerUsecase(Usecase):
    """フォロワー一覧を取得。"""
    def __init__(self, account_service: AccountDomainService):
        self.account_service = account_service

    def execute(self, id):
        account: Account = self.account_service.get_account_by_id(id)
        account_ids = account.followers.all().values_list('follower', flat=True)
        accounts = Account.objects.filter(id__in=account_ids)


        return {
            "accounts": accounts,
            "account": account,
        }

class GetFollowingsUsecase(Usecase):
    """フォロー一覧を取得。"""
    def __init__(self, account_service: AccountDomainService):
        self.account_service = account_service

    def execute(self, id):
        account: Account = self.account_service.get_account_by_id(id)

        account_ids = account.following.all().values_list('followed', flat=True)
        accounts = Account.objects.filter(id__in=account_ids)

        return {
            "accounts": accounts,
            "account": account,
        }



class FollowAccountUsecase(Usecase):
    """アカウントをフォローする。"""
    def __init__(self, account_service:AccountDomainService, follow_service: FollowService):
        self.account_service = account_service
        self.follow_service = follow_service

    def execute(self, user, target_id):
        target_account = self.account_service.get_account_by_id(target_id)

        if user == target_account:
            raise Account.DoesNotExist("自分自身はフォローできません。")

        followed = self.follow_service.follow(user, target_account)

        # TODO followedを値で返したい
        return {"followed": True}

class UnfollowAccountUsecase(Usecase):
    """アカウントのフォローを解除する。"""
    def __init__(self, account_service:AccountDomainService, follow_service: FollowService):
        self.account_service = account_service
        self.follow_service = follow_service

    def execute(self, user, target_id):
        target_account = self.account_service.get_account_by_id(target_id)

        if user == target_account:
            raise Account.DoesNotExist("自分自身はフォロー解除できません。")

        unfollowed = self.follow_service.unfollow(user, target_account)

        return {"unfollowed": unfollowed}
