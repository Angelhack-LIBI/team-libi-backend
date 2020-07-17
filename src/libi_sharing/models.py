from django.db import models

from src.libi_account.models import Account
from src.libi_common.models import BaseModel


class Sharing(models.Model, BaseModel):
    sharing_id = models.IntegerField(primary_key=True, auto_created=True)
    title = models.CharField(default='NONE', blank=True, max_length=200)
    description = models.TextField(default='NONE', blank=True)
    unit_mapping_id = models.ForeignKey(Unit, null=True, on_delete=models.SET_NULL)
    location_id = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)
    category_id = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    created_user_id = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)
