from enum import IntEnum

from django.db import models

from libi_common.models import BaseModel, ImageMixin


class SharingType(IntEnum):
    FUNDING = 1  # 공구
    STOCKSALE = 2  # 재고할인


class Sharing(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    area = models.ForeignKey('Area', null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey('Category', null=True, on_delete=models.SET_NULL)
    created_account = models.ForeignKey('libi_account.Account', null=True, on_delete=models.SET_NULL)
    goal_price = models.IntegerField()
    sharing_type = models.IntegerField()


class Category(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)


class SharingOption(BaseModel):
    sharing = models.ForeignKey('Sharing', related_name='options', null=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=16,help_text='상품 판매 단위')
    price = models.IntegerField(help_text='상품 판매 단위당 가격')


class AreaGroup(BaseModel):
    name = models.CharField(max_length=50)


class Area(BaseModel):
    group = models.ForeignKey('AreaGroup', null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)


class SharingPhoto(BaseModel, ImageMixin):
    FILE_UPLOAD_PATH = 'sharing_photo'
    sharing = models.ForeignKey('Sharing', null=True, related_name='photos', on_delete=models.SET_NULL)


class SharingApply(BaseModel):
    account = models.ForeignKey('libi_account.Account', null=True, on_delete=models.SET_NULL)
    sharing = models.ForeignKey('Sharing', null=True, on_delete=models.SET_NULL)
    sharing_option = models.ForeignKey('SharingOption', null=True, on_delete=models.SET_NULL)
    apply_amount = models.IntegerField()
    apply_price = models.IntegerField()
