from authentication.models import Account


class AccountRepository(object):
    def fetch_account_by_id(self, id):
        return Account.objects.get(id=id)