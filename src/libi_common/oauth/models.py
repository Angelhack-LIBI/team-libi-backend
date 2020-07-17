from __future__ import annotations

from dataclasses import dataclass

import pendulum
from django.conf import settings

from libi_common.utils import now


@dataclass()
class StatelessAccount:
    id: int
    phone: str
    name: str
    is_staff: bool

    @classmethod
    def from_stateful_account(cls, account) -> StatelessAccount:
        return cls(
            id=account.id,
            phone=account.phone,
            name=account.get_full_name(),
            is_staff=account.is_staff,
        )


class TokenConfig:
    ISSUER = 'libi'
    SUBJECT = 'libi_accesstoken'
    ALGORITHM = 'HS384'
    SECRET_KEY = settings.SECRET_KEY


@dataclass()
class TokenPayload:
    iss: str
    sub: str
    exp: int
    iat: int
    account: StatelessAccount

    @classmethod
    def factory(cls, account: StatelessAccount, expire_at: pendulum.DateTime):
        return cls(
            iss=TokenConfig.ISSUER,
            sub=TokenConfig.SUBJECT,
            exp=int(expire_at.timestamp()),
            iat=int(now().timestamp()),
            account=account,
        )
