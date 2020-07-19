from typing import List

from django.db.models import Sum
from rest_framework import serializers

from libi_account.models import Account
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
    area_id = serializers.IntegerField(required=True, help_text='지역 코드 (`area/me` api 에서 받은 지역코드 이용)')
    keyword = serializers.CharField(required=False, help_text='검색 키워드')
    size = serializers.IntegerField(default=20, help_text='페이지 당 항목 개수')
    last_id = serializers.IntegerField(default=0, help_text='마지막으로 불러온 항목의 id')


class SharingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharingOption
        fields = ('id', 'description', 'price')


class SharingListAttributeSerializer(StatelessSerializer):
    title = serializers.CharField(required=True, help_text='쉐어링 특성 부제')
    content = serializers.CharField(required=True, help_text='쉐어링 특성 내용')
    is_focused = serializers.BooleanField(default=False, help_text='쉐어링 특성 하이라이트 여부')


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
        if obj.sharing_type == SharingType.FUNDING:
            min_price = obj.options.first().price
            sum_price = obj.applies.aggregate(Sum('apply_price')).get('apply_price__sum') or 0
            ratio = int((sum_price / obj.goal_price) * 100) if 0 < sum_price else 0
            return SharingListAttributeSerializer([
                dict(title='단위금액', content=f"{min_price:,}원", is_focused=True),
                dict(title='달성률', content=f'{ratio}%', is_focused=100 <= ratio)
            ], many=True).data

        if obj.sharing_type == SharingType.STOCKSALE:
            price = obj.options.first().price
            return SharingListAttributeSerializer([
                dict(title='희망금액', content=f"{price:,}원", is_focused=True)
            ], many=True).data

        if obj.sharing_type == SharingType.AD:
            return SharingListAttributeSerializer([
                dict(title='by', content="스폰서 광고", is_focused=True)
            ], many=True).data


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
        fields = ('id', 'title', 'sharing_type', 'category_id', 'goal_price', 'description', 'option',
                  'photo_urls', 'achievement')
        read_only_fields = ('id', 'title', 'sharing_type', 'category_id', 'goal_price', 'description',
                            'option', 'photo_urls', 'achievement')

    option = serializers.SerializerMethodField()
    photo_urls = serializers.SerializerMethodField()
    achievement = serializers.SerializerMethodField(help_text="목표 달성률")

    def get_option(self, obj: Sharing) -> SharingOptionSerializer:
        return SharingOptionSerializer(obj.options.first()).data

    def get_photo_urls(self, obj: Sharing) -> List[str]:
        urls = []
        for photo in obj.photos.filter(deleted_at=None).all():
            url = photo.file.url if getattr(photo, 'file', None) else ''
            if url:
                urls.append(url)
        return urls

    def get_achievement(self, obj: Sharing):
        sum_price = obj.applies.aggregate(Sum('apply_price')).get('apply_price__sum') or 0
        return int((sum_price / obj.goal_price) * 100) if 0 < sum_price else 0


class SharingApplySerializer(StatelessSerializer):
    number = serializers.IntegerField(min_value=1)


class SharingContactUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('phone', 'name')


class SharingApplyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharingApply
        fields = ('id', 'sharing', 'sharing_option', 'apply_amount', 'apply_price')
