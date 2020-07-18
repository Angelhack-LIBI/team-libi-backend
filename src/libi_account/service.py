from typing import Optional, Tuple

from libi_common.utils import now
from libi_account.models import Account, AccountToken
from libi_account.errors import (
    DuplicateAccountError,
    NotExistAccountError,
    NotExistTokenError,
)
from libi_common.oauth.models import StatelessAccount


def create_account(phone: str, password: str) -> Account:
    """
    신규 계정을 생성합니다
    :return: 신규 계정 인스턴스
    :rtype: Account
    """
    if Account.objects.filter(phone=phone, deleted_at=None).exists():
        raise DuplicateAccountError()

    new_account = Account.objects.create_user(phone, password)
    return new_account


def find_account(phone: str, password: Optional[str] = None) -> Account:
    """
    이미 존재하는 계정을 찾습니다
    :return: 찾은 계정 인스턴스
    :rtype: Account
    """
    account = Account.objects.filter(
        phone=phone,
        deleted_at=None,
    ).first()
    if not account:
        raise NotExistAccountError()

    if password is not None and not account.check_password(password):
        raise NotExistAccountError()

    return account


def create_token_set(account: Account) -> Tuple[str, AccountToken]:
    """
    신규 토큰 세트를 발급합니다
    :param account: 토큰 발급할 계정
    :return: 발급된 토큰 (accessToken, refreshToken)
    :rtype: tuple
    """
    token = AccountToken.factory(account.id)
    access_token = token.issue_access_token()
    token.save()
    return access_token, token


def refresh_access_token(refresh_token: str) -> str:
    """
    Refresh Token으로 access token 갱신
    :param refresh_token:
    :return: 갱신된 access token
    :rtype: str
    """
    if not refresh_token:
        raise NotExistTokenError()

    account_token: AccountToken = AccountToken.objects.filter(
        refresh_token=refresh_token,
        expire_at__gt=now(),
    ).first()
    if not account_token:
        raise NotExistTokenError()

    new_access_token = account_token.issue_access_token()
    account_token.save()
    return new_access_token


def expire_token(refresh_token: str):
    """
    RefreshToken을 만료시킵니다
    :param refresh_token: RefreshToken
    """
    if not refresh_token:
        return

    account_token: AccountToken = AccountToken.objects.filter(
        refresh_token=refresh_token,
        expire_at__gt=now(),
    ).first()
    account_token.expire_at = now()
    account_token.save()
