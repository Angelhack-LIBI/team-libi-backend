from django.http.cookie import SimpleCookie
from django.shortcuts import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from libi_account.models import Account, AccountToken
from libi_common.utils import now
from libi_common.oauth.models import TokenPayload
from libi_common.oauth.utils import extract_access_token


class AccountRootViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.account_data = {
            'phone': '01012345678',
            'password': 'password?',
        }
        self.account = Account.objects.create_user(**self.account_data)

    def test_password_is_hashed(self):
        self.assertNotEqual(self.account_data['password'], self.account.password)

    def test_duplicate_account_block(self):
        """
        휴대전화번호 중복가입 방지 체크
        """
        res = self.client.post(reverse('libi_account:account'), {
            'phone': self.account_data['phone'],
            'password': 'dontallowme',
        })
        self.assertEqual(res.status_code, status.HTTP_409_CONFLICT)

    def test_create(self):
        """
        가입 후 유저 생성 확인
        """
        res = self.client.post(reverse('libi_account:account'), {
            'phone': '01099998888',
            'password': 'testtest',
        })
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        account_id = res.data['id']

        account = Account.objects.filter(id=account_id, deleted_at=None).first()
        self.assertIsNotNone(account)


class TokenRootViewTest(TestCase):
    def setUp(self):
        self.account_data = {
            'phone': '01012345678',
            'password': 'password?',
        }
        self.account = Account.objects.create_user(**self.account_data)

    def test_invalid_account(self):
        """
        유효하지 않은 계정 토큰 발급 테스트
        """
        client = APIClient()
        res = client.post(reverse('libi_account:token'), {
            'phone': '01011112222',
        })
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        res = client.post(reverse('libi_account:token'), {
            'phone': '01011112222',
            'password': '   ',
        })
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        res = client.post(reverse('libi_account:token'), {
            'phone': '     ',
            'password': 'password',
        })
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        res = client.post(reverse('libi_account:token'), {
            'phone': self.account_data['phone'],
            'password': 'password',
        })
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_generate(self):
        """
        토큰 정상 발급 테스트
        """
        client = APIClient()
        res = client.post(reverse('libi_account:token'), self.account_data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        access_token = res.data.get('access_token', '')
        refresh_token_cookie = res.cookies.get('libi_refreshtoken', None)
        self.assertIsNotNone(refresh_token_cookie)
        refresh_token = refresh_token_cookie.value
        self.assertGreater(len(access_token), 1)
        self.assertGreater(len(refresh_token), 1)

        token_payload = extract_access_token(access_token)
        self.assertIsInstance(extract_access_token(access_token), TokenPayload)
        self.assertEqual(token_payload.account.id, self.account.id)

        token_row_exists = AccountToken.objects.filter(refresh_token=refresh_token, expire_at__gt=now()).exists()
        self.assertTrue(token_row_exists)

    def test_token_refresh(self):
        """
        토큰 Refresh 테스트
        """
        account_token = AccountToken.factory(self.account.id)
        account_token.save()

        client = APIClient()
        client.cookies = SimpleCookie({'libi_refreshtoken': 'invalid'})

        res = client.put(reverse('libi_account:token'))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        client.cookies = SimpleCookie({'libi_refreshtoken': account_token.refresh_token})

        res = client.put(reverse('libi_account:token'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        access_token = res.data.get('access_token', '')
        self.assertGreater(len(access_token), 1)

        token_payload = extract_access_token(access_token)
        self.assertIsInstance(extract_access_token(access_token), TokenPayload)
        self.assertEqual(token_payload.account.id, self.account.id)

    def test_delete_token(self):
        """
        토큰 만료 (로그아웃) 테스트
        """
        account_token = AccountToken.factory(self.account.id)
        account_token.save()

        client = APIClient()
        client.cookies = SimpleCookie({'libi_refreshtoken': account_token.refresh_token})

        res = client.delete(reverse('libi_account:token'))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
