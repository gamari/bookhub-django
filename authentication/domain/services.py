from authentication.domain.repositories import AccountRepository


class AccountDomainService(object):
    def __init__(self, account_repo: AccountRepository):
        self.account_repo = account_repo

    def get_account_by_id(self, id):
        return self.account_repo.fetch_account_by_id(id)