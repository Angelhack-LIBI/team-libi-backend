from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from libi_account.serializers import (
    AccountCreateRequestSerializer,
    AccountSerializer,
    TokenCreateRequestSerializer,
    TokenResponseSerializer,
)
from libi_account.service import (
    create_account,
    find_account,
    create_token_set,
    refresh_access_token,
    expire_token,
)
from libi_common.utils import datetime_to_pendulum


class AccountView(APIView):
    def post(self, request: Request) -> Response:
        """
        계정 생성 API
        """
        serializer = AccountCreateRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_account = create_account(**serializer.validated_data)
        response_serializer = AccountSerializer(new_account)
        return Response(
            data=response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class TokenView(APIView):
    def post(self, request: Request) -> Response:
        """
        토큰 발급 (로그인) API
        """
        if request.user.id:
            # 이미 인증되어 있는 경우 자신의 토큰을 반환
            response_serializer = TokenResponseSerializer(data={'access_token': request.access_token})
            if not response_serializer.is_valid(raise_exception=False):
                raise PermissionDenied()
            response = Response(
                data=response_serializer.data,
                status=status.HTTP_304_NOT_MODIFIED,
            )
            return response

        serializer = TokenCreateRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = find_account(serializer.validated_data['phone'], serializer.validated_data['password'])
        access_token, account_token = create_token_set(account)

        response_serializer = TokenResponseSerializer(data={'access_token': access_token})
        if not response_serializer.is_valid(raise_exception=False):
            raise PermissionDenied()
        response = Response(
            data=response_serializer.data,
            status=status.HTTP_201_CREATED,
        )
        response.set_cookie(
            'libi_refreshtoken',
            value=account_token.refresh_token,
            expires=datetime_to_pendulum(account_token.expire_at).to_iso8601_string(),
            path='/',
            httponly=True,
        )
        return response

    def put(self, request: Request) -> Response:
        """
        토큰 갱신 API
        """
        if request.user.id:
            # 이미 인증되어 있는 경우 자신의 토큰을 반환
            response_serializer = TokenResponseSerializer(data={'access_token': request.access_token})
            if not response_serializer.is_valid(raise_exception=False):
                raise PermissionDenied()
            response = Response(
                data=response_serializer.data,
                status=status.HTTP_304_NOT_MODIFIED,
            )
            return response

        refresh_token = request.COOKIES.get('libi_refreshtoken')
        access_token = refresh_access_token(refresh_token)
        response_serializer = TokenResponseSerializer(data={'access_token': access_token})
        if not response_serializer.is_valid(raise_exception=False):
            raise PermissionDenied()
        response = Response(
            data=response_serializer.data,
            status=status.HTTP_200_OK,
        )
        return response

    def delete(self, request: Request) -> Response:
        refresh_token = request.COOKIES.get('libi_refreshtoken')
        expire_token(refresh_token)
        return Response(status=status.HTTP_204_NO_CONTENT)
