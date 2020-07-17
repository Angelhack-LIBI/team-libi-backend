from django.shortcuts import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from libi_account.models import Account


class AccountRootViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.account_data = {
            'phone': '01012345678',
            'password': 'password?',
        }
        Account.objects.create_user(**self.account_data)

    def test_duplicate_account_block(self):
        """
        휴대전화번호 중복가입 방지 체크
        """
        res = self.client.post(reverse('libi_account:account_root'), {
            'phone': self.account_data['phone'],
            'password': 'dontallowme',
        })
        self.assertEqual(res.status_code, status.HTTP_409_CONFLICT)

    def test_create(self):
        """
        가입 후 유저 생성 확인
        """
        res = self.client.post(reverse('libi_account:account_root'), {
            'phone': '01099998888',
            'password': 'testtest',
        })
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        account_id = res.data['id']

        account = Account.objects.filter(id=account_id, deleted_at=None).first()
        self.assertIsNotNone(account)
