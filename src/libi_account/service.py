from libi_account.models import Account
from libi_account.errors import DuplicateAccountError


def create_account(phone: str, password: str) -> Account:
    if Account.objects.filter(phone=phone, deleted_at=None).exists():
        raise DuplicateAccountError()

    new_account = Account.objects.create_user(phone, password)
    return new_account
