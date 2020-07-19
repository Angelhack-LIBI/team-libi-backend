from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from libi_common.serializers import APIErrorSerializer
from libi_sharing.models import Sharing, Area, Category, SharingApply, SharingOption
from libi_sharing.serializers import (
    AreaSerializer,
    CategorySerializer,
    SharingListFilterSerializer,
    SharingListItemSerializer,
    SharingCreateRequestSerializer,
    SharingDetailItemSerializer,
    SharingApplyDetailSerializer, SharingApplySerializer, SharingContactUserSerializer)
from libi_sharing.service import create_sharing, get_sharing


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
        request_serializer = SharingListFilterSerializer(data=request.query_params)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data

        queryset = Sharing.objects

        if validated_data.get('area_id'):
            queryset = queryset.filter(area_id=validated_data['area_id'])

        if validated_data.get('keyword'):
            keyword = validated_data['keyword']
            queryset = queryset.filter(title__contains=keyword)

        if validated_data['last_id'] > 0:
            queryset = queryset.filter(id__lt=validated_data['last_id'])
        queryset = queryset.order_by('-id').all()[:validated_data['size']]

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
        if not request.user:
            raise PermissionDenied()

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
        return Response(
            data=SharingDetailItemSerializer(get_sharing(sharing_id)).data,
            status=status.HTTP_200_OK
        )


class SharingApplyView(APIView):
    @swagger_auto_schema(
        operation_summary="공동구매 apply",
        request_body=SharingApplySerializer,
        responses={
            status.HTTP_200_OK: SharingApplyDetailSerializer,
            status.HTTP_404_NOT_FOUND: APIErrorSerializer,
        }
    )
    def post(self, request: Request, sharing_id: int) -> Response:
        request_serializer = SharingApplySerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        amount_number = request_serializer.data.get('number')
        sharing = get_sharing(sharing_id)
        sharing_option: SharingOption = sharing.options.first()
        new_apply = SharingApply.objects.create(account_id=request.user.id, sharing=sharing,
                                                sharing_option=sharing.options.first(),
                                                apply_amount=amount_number,
                                                apply_price=sharing_option.price * amount_number)
        return Response(
            data=SharingApplyDetailSerializer(new_apply).data,
            status=status.HTTP_200_OK
        )


class SharingContactView(APIView):
    @swagger_auto_schema(
        operation_summary="재고할인 연락하기",
        responses={
            status.HTTP_200_OK: SharingContactUserSerializer,
            status.HTTP_404_NOT_FOUND: APIErrorSerializer,
        }
    )
    def get(self, request: Request, sharing_id: int) -> Response:
        user = get_sharing(sharing_id).created_account
        return Response(
            data=SharingContactUserSerializer(user).data,
            status=status.HTTP_200_OK
        )


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
