from drf_yasg.utils import swagger_auto_schema
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
from libi_common.serializers import APIErrorSerializer
from libi_common.utils import datetime_to_pendulum


class AccountView(APIView):
    @swagger_auto_schema(
        operation_summary="신규 계정 생성",
        request_body=AccountCreateRequestSerializer,
        responses={
            status.HTTP_201_CREATED: AccountSerializer,
            status.HTTP_400_BAD_REQUEST: APIErrorSerializer,
            status.HTTP_409_CONFLICT: APIErrorSerializer,
        }
    )
    def post(self, request: Request) -> Response:
        serializer = AccountCreateRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_account = create_account(**serializer.validated_data)
        response_serializer = AccountSerializer(new_account)
        return Response(
            data=response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class TokenView(APIView):
    @swagger_auto_schema(
        operation_summary="토큰 발급 (로그인)",
        request_body=TokenCreateRequestSerializer,
        responses={
            status.HTTP_201_CREATED: TokenResponseSerializer,
            status.HTTP_304_NOT_MODIFIED: TokenResponseSerializer,
            status.HTTP_400_BAD_REQUEST: APIErrorSerializer,
            status.HTTP_403_FORBIDDEN: APIErrorSerializer,
        }
    )
    def post(self, request: Request) -> Response:
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

    @swagger_auto_schema(
        operation_summary="토큰 갱신",
        request_body=None,
        responses={
            status.HTTP_200_OK: TokenResponseSerializer,
            status.HTTP_304_NOT_MODIFIED: TokenResponseSerializer,
            status.HTTP_400_BAD_REQUEST: APIErrorSerializer,
            status.HTTP_403_FORBIDDEN: APIErrorSerializer,
        }
    )
    def put(self, request: Request) -> Response:
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

    @swagger_auto_schema(
        operation_summary="토큰 만료 (로그아웃)",
        request_body=None,
        responses={
            status.HTTP_204_NO_CONTENT: None,
        }
    )
    def delete(self, request: Request) -> Response:
        refresh_token = request.COOKIES.get('libi_refreshtoken')
        expire_token(refresh_token)
        return Response(status=status.HTTP_204_NO_CONTENT)
