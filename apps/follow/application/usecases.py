from authentication.domain.services import AccountDomainService

from config.application.usecases import Usecase

class ShowFollowerPage(Usecase):
    def __init__(self, account_service: AccountDomainService):
        self.account_service = account_service

    def execute(self, id):
        account = self.account_service.get_account_by_id(id)
        followers = account.followers.all()

        return {
            "followers": followers,
            "account": account,
        }