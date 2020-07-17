from __future__ import annotations

from dataclasses import dataclass


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


class AccessToken:
    ALGORITHM = 'HS384'
    ISSUER = 'handys_account'
    EXPIRE_TIME = {'hour': 1}
