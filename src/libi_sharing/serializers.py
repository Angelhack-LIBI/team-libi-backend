from rest_framework import serializers

from libi_common.serializers import StatelessSerializer
from libi_sharing.models import (
    Area,
    Category,
    Sharing,
    SharingOption
)


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ('id', 'name')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title')


class SharingListFilterSerializer(StatelessSerializer):
    area_id = serializers.IntegerField(required=True, help_text='지역 코드')
    keyword = serializers.CharField(required=False, help_text='검색 키워드')


class SharingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharingOption
        fields = ('id', 'description', 'minimum_price', 'price')


class SharingListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sharing
        fields = ('id', 'title', 'sharing_type', 'goal_price', 'thumbnail_url', 'option',)
        read_only_fields = ('id', 'title', 'sharing_type', 'goal_price', 'thumbnail_url', 'option',)

    thumbnail_url = serializers.SerializerMethodField(read_only=True, help_text='대표 이미지 url')
    option = serializers.SerializerMethodField(read_only=True, help_text='쉐어링 대표 옵션')

    def get_thumbnail_url(self, obj: Sharing) -> str:
        pass

    def get_option(self, obj: Sharing) -> SharingOptionSerializer:
        pass
