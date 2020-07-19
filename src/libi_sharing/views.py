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

# Create your views here.
