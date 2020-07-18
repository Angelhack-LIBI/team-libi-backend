from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from libi_common.serializers import APIErrorSerializer
from libi_sharing.serializers import (
    AreaSerializer,
    CategorySerializer,
    SharingListFilterSerializer,
    SharingListItemSerializer,
    SharingCreateRequestSerializer,
    SharingDetailItemSerializer,
)


class SharingRootView(APIView):
    @swagger_auto_schema(
        operation_summary="쉐어링 리스트",
        query_serializer=SharingListFilterSerializer,
        responses={
            status.HTTP_200_OK: SharingListItemSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: APIErrorSerializer,
        }
    )
    def get(self, request: Request) -> Response:
        pass

    @swagger_auto_schema(
        operation_summary="쉐어링 등록",
        request_body=SharingCreateRequestSerializer,
        responses={
            status.HTTP_200_OK: SharingListItemSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: APIErrorSerializer,
        }
    )
    def get(self, request: Request) -> Response:
        pass


class SharingItemView(APIView):
    @swagger_auto_schema(
        operation_summary="쉐어링 상세 조회",
        responses={
            status.HTTP_200_OK: SharingDetailItemSerializer,
            status.HTTP_404_NOT_FOUND: APIErrorSerializer,
        }
    )
    def get(self, request: Request, sharing_id: int) -> Response:
        pass


class SharingApplyView(APIView):
    def get(self, request: Request, sharing_id: int) -> Response:
        pass


class SharingContactView(APIView):
    def get(self, request: Request, sharing_id: int) -> Response:
        pass


class MyAreaView(APIView):
    @swagger_auto_schema(
        operation_summary="내 지역 조회",
        responses={
            status.HTTP_200_OK: AreaSerializer,
            status.HTTP_404_NOT_FOUND: APIErrorSerializer,
        }
    )
    def get(self, request: Request) -> Response:
        # 더미로 위치 정보를 받는 척 하고, 현재 area를 돌려주는 API
        pass


class CategoryView(APIView):
    @swagger_auto_schema(
        operation_summary="전체 카테고리 목록",
        responses={
            status.HTTP_200_OK: CategorySerializer(many=True),
        }
    )
    def get(self, request: Request) -> Response:
        pass
