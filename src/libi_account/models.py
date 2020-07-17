from __future__ import annotations

import secrets

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from libi_common.models import BaseModel, SimpleBaseModel
from libi_common.utils import now, datetime_to_pendulum
from libi_common.oauth.models import StatelessAccount
from libi_common.oauth.utils import generate_access_token


class AccountManager(BaseUserManager):
    def create_user(self, phone: str, password=None, **kwargs) -> models.Model:
        if not phone:
            raise ValueError('Email is required.')

        user = self.model(
            phone=phone,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone: str, password=None, **kwargs) -> models.Model:
        user = self.create_user(phone, password, is_staff=True, **kwargs)
        return user


class Account(BaseModel, AbstractBaseUser, PermissionsMixin):
    # Django User Configuration
    objects = AccountManager()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name', ]

    phone = models.CharField(max_length=16, unique=True, help_text="휴대전화번호")
    name = models.CharField(max_length=64, help_text="이름")

    is_staff = models.BooleanField(null=False, default=False, help_text="관리자 여부")

    @property
    def is_active(self) -> bool:
        return not self.is_deleted

    def get_full_name(self) -> str:
        return self.name

    def get_short_name(self) -> str:
        return self.get_full_name()


class AccountToken(SimpleBaseModel):
    # Token Configuration
    REFRESH_TOKEN_EXPIRE_TIME = {'year': 1}
    ACCESS_TOKEN_EXPIRE_TIME = {'hour': 1}

    account = models.ForeignKey('Account', on_delete=models.CASCADE, help_text='토큰 발급 계정')
    refresh_token = models.CharField(max_length=43, unique=True, help_text="RefreshToken")
    refreshed_at = models.DateTimeField(auto_now_add=True, help_text="토큰 갱신 일시")
    expire_at = models.DateTimeField(null=True, help_text="토큰 만료 일시")

    @property
    def is_active(self) -> bool:
        return now() < datetime_to_pendulum(self.expire_at)

    @classmethod
    def factory(cls, account_id: int) -> AccountToken:
        instance = cls()
        instance.account_id = account_id
        instance.refresh_token = instance.issue_refresh_token()
        instance.expire_at = now().add(**cls.REFRESH_TOKEN_EXPIRE_TIME)
        return instance

    def issue_refresh_token(self) -> str:
        return secrets.token_urlsafe(32)

    def issue_access_token(self) -> str:
        token = generate_access_token(
            StatelessAccount.from_stateful_account(self.account),
            self.ACCESS_TOKEN_EXPIRE_TIME,
            datetime_to_pendulum(self.expire_at)
        )
        self.refreshed_at = now()
        self.save()
        return token
