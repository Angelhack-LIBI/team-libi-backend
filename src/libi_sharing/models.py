from django.db import models

from libi_common.models import BaseModel


class Sharing(BaseModel):
    title = models.CharField(blank=False, max_length=200)
    description = models.TextField(blank=True)
    unit_mapping_id = models.ForeignKey('libi_sharing.models.SharingOption', null=True, on_delete=models.SET_NULL)
    section_id = models.ForeignKey('Section', null=True, on_delete=models.SET_NULL)
    category_id = models.ForeignKey('Category', null=True, on_delete=models.SET_NULL)
    created_user_id = models.ForeignKey('libi_account.Account', null=True, on_delete=models.SET_NULL)
    price = models.IntegerField(default=0)
    sharing_type = models.IntegerField(blank=False, null=False)


class Category(BaseModel):
    title = models.CharField(blank=False, max_length=200)
    description = models.TextField(blank=True)


class SharingOption(BaseModel):
    description = models.CharField(blank=False, max_length=16)
    minimum_price = models.IntegerField(default=0)
    price = models.IntegerField(default=0)


class SectionGroup(BaseModel):
    name = models.CharField(blank=False, max_length=50)


class Section(BaseModel):
    section_group_id = models.ForeignKey('SectionGroup', null=False, on_delete=models.SET_NULL)
    name = models.CharField(blank=False, max_length=100)


class FIleGroup(BaseModel):
    funding_id = models.ForeignKey('Sharing', null=True, on_delete=models.SET_NULL)
    file_id = models.ForeignKey('File', null=True, on_delete=models.SET_NULL)


class File(BaseModel):
    extension = models.CharField(blank=False, max_length=30)
    file_type = models.CharField(blank=False, max_length=10)
    name = models.CharField(blank=False, max_length=100)
    path = models.CharField(blank=False, max_length=200)
    size = models.IntegerField(default=0)


class ApplyGroup(BaseModel):
    funding_id = models.ForeignKey('Sharing', null=True, on_delete=models.SET_NULL)
    apply_id = models.ForeignKey('Apply', null=True, on_delete=models.SET_NULL)


class Apply(BaseModel):
    user_id = models.ForeignKey('libi_account.Account', null=True, on_delete=models.SET_NULL)
    funding_count = models.IntegerField(default=0)
    funding_price = models.IntegerField(default=0)
    state = models.CharField(blank=False, max_length=10)
