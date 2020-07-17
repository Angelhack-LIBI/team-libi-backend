from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from libi_account.errors import DuplicateAccountError
from libi_account.serializers import (
    AccountCreateRequestSerializer, AccountSerializer
)
from libi_account.service import create_account


class AccountRootView(APIView):
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
