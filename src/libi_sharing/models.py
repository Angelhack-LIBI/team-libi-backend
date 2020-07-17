from django.db import models

from libi_common.models import BaseModel


class Funding(BaseModel):
    title = models.CharField(blank=False, max_length=200)
    description = models.TextField(blank=True)
    unit_mapping_id = models.ForeignKey('FundingOption', null=True, on_delete=models.SET_NULL)
    section_id = models.ForeignKey('Section', null=True, on_delete=models.SET_NULL)
    category_id = models.ForeignKey('Category', null=True, on_delete=models.SET_NULL)
    created_user_id = models.ForeignKey('libi_account.Account', null=True, on_delete=models.SET_NULL)
    file = models.ForeignKey('File', null=True, on_delete=models.SET_NULL)


class Category(BaseModel):
    title = models.CharField(blank=False, max_length=200)
    description = models.TextField(blank=True)


class FundingOption(BaseModel):
    description = models.CharField(blank=False, max_length=16)
    minimum_price = models.IntegerField(default=0)
    price = models.IntegerField(default=0)


class SectionGroup(BaseModel):
    name = models.CharField(blank=False, max_length=50)


class Section(BaseModel):
    section_group_id = models.ForeignKey('SectionGroup', null=False, on_delete=models.SET_NULL)
    name = models.CharField(blank=False, max_length=100)


class File(BaseModel):
    extension = models.CharField(blank=False, max_length=30)
    file_type = models.CharField(blank=False, max_length=10)
    name = models.CharField(blank=False, max_length=100)
    path = models.CharField(blank=False, max_length=200)
    size = models.IntegerField(default=0)
