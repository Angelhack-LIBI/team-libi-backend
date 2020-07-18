from typing import List

from rest_framework import serializers

from libi_common.serializers import StatelessSerializer
from libi_sharing.models import (
    Area,
    Category,
    Sharing,
    SharingType,
    SharingOption,
    SharingPhoto, SharingApply)


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ('id', 'name')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title')


class SharingListFilterSerializer(StatelessSerializer):
    area_id = serializers.IntegerField(required=True, help_text='지역 코드(개발 서버에서는 1로 고정)')
    keyword = serializers.CharField(required=False, help_text='검색 키워드')


class SharingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharingOption
        fields = ('id', 'description', 'price')


class SharingListAttributeSerializer(StatelessSerializer):
    title = serializers.CharField(required=True, help_text='쉐어링 특성 부제')
    content = serializers.CharField(required=True, help_text='쉐어링 특성 내용')
    is_focused = serializers.BooleanField(required=True, default=False, help_text='쉐어링 특성 하이라이트 여부')


class SharingListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sharing
        fields = ('id', 'title', 'sharing_type', 'thumbnail_url', 'attributes')
        read_only_fields = ('id', 'title', 'sharing_type', 'thumbnail_url', 'attributes')

    thumbnail_url = serializers.SerializerMethodField(read_only=True, help_text='대표 이미지 url')
    attributes = serializers.SerializerMethodField(read_only=True, help_text='쉐어링 하단 특성 목록')

    def get_thumbnail_url(self, obj: Sharing) -> str:
        photo: SharingPhoto = obj.photos.first()
        return photo.file.url

    def get_attributes(self, obj: Sharing) -> SharingListAttributeSerializer(many=True):
        pass


class SharingCreateRequestSerializer(StatelessSerializer):
    sharing_type = serializers.ChoiceField(required=True, choices=[t.value for t in SharingType], help_text='쉐어링 유형')
    area_id = serializers.IntegerField(required=True, help_text='지역 코드')
    title = serializers.CharField(required=True, max_length=200, help_text='상품명')
    category_id = serializers.IntegerField(required=True, help_text='카테고리 id')
    goal_price = serializers.IntegerField(required=False, default=0, min_value=0, help_text='목표 금액')
    description = serializers.CharField(required=True, help_text='상품 상세 설명')
    option_description = serializers.CharField(required=True, max_length=14, help_text='상품 판매 단위')
    option_price = serializers.IntegerField(required=True, help_text='상품 판매 단위당 가격')
    photo = serializers.ListField(child=serializers.ImageField(), allow_empty=False, min_length=1, max_length=10)


class SharingDetailItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sharing
        fields = ('id', 'title', 'sharing_type', 'category_id', 'goal_price', 'description', 'option', 'photo_urls')
        read_only_fields = ('id', 'title', 'sharing_type', 'category_id', 'goal_price', 'description', 'option', 'photo_urls')

    option = serializers.SerializerMethodField()
    photo_urls = serializers.SerializerMethodField()

    def get_option(self, obj: Sharing) -> SharingOptionSerializer:
        pass

    def get_photo_urls(self, obj: Sharing) -> List[str]:
        urls = []
        print(obj.photos)
        for photo in obj.photos.filter(deleted_at=None).all():
            url = photo.file.url if getattr(photo, 'file', None) else ''
            if url:
                urls.append(url)
        return urls


class SharingApplyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharingApply
        fields = ('id', 'sharing', 'sharing_option', 'apply_account', 'apply_price')
