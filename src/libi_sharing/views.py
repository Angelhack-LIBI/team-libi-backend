from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from libi_common.serializers import APIErrorSerializer
from libi_sharing.models import Sharing, Area, Category
from libi_sharing.serializers import (
    AreaSerializer,
    CategorySerializer,
    SharingListFilterSerializer,
    SharingListItemSerializer,
    SharingCreateRequestSerializer,
    SharingDetailItemSerializer,
    SharingApplyDetailSerializer)
from libi_sharing.service import create_sharing, find_sharing


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
        """
        list Sharing items
        """
        queryset = Sharing.objects.all()
        response_serializer = SharingListItemSerializer(queryset, many=True)

        return Response(
            data=response_serializer.data,
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_summary="쉐어링 등록 (form-data로 보내야 함)",
        request_body=SharingCreateRequestSerializer,
        responses={
            status.HTTP_200_OK: SharingDetailItemSerializer,
            status.HTTP_400_BAD_REQUEST: APIErrorSerializer,
        }
    )
    def post(self, request: Request) -> Response:
        """
        create Sharing
        """
        request_serializer = SharingCreateRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        new_sharing = create_sharing(**request_serializer.validated_data, created_account_id=request.user.id)

        response_serializer = SharingDetailItemSerializer(new_sharing)
        return Response(
            data=response_serializer.data,
            status=status.HTTP_200_OK,
        )


class SharingItemView(APIView):
    @swagger_auto_schema(
        operation_summary="쉐어링 상세 조회",
        responses={
            status.HTTP_200_OK: SharingDetailItemSerializer,
            status.HTTP_404_NOT_FOUND: APIErrorSerializer,
        }
    )
    def get(self, request: Request, sharing_id: int) -> Response:
        reuqest_serializer, response_serializer = None, None
        if request.query_params.get('pk'):
            reuqest_serializer = SharingDetailItemSerializer(data=sharing_id)
            reuqest_serializer.is_valid(raise_exception=True)

            sharing = find_sharing(reuqest_serializer.validated_data['id'])
            response_serializer = SharingDetailItemSerializer(sharing)

        return Response(
            data=response_serializer.data,
            status=status.HTTP_200_OK
        )


class SharingApplyView(APIView):
    @swagger_auto_schema(
        operation_summary="쉐어링 지원 상세 조회",
        response={
            status.HTTP_200_OK: SharingApplyDetailSerializer,
            status.HTTP_404_NOT_FOUND: APIErrorSerializer,
        }
    )
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
        return Response(AreaSerializer(Area.objects.get(id=1)).data)


class CategoryView(APIView):
    @swagger_auto_schema(
        operation_summary="전체 카테고리 목록",
        responses={
            status.HTTP_200_OK: CategorySerializer(many=True),
        }
    )
    def get(self, request: Request) -> Response:
        return Response(CategorySerializer(Category.objects.all(), many=True).data)
