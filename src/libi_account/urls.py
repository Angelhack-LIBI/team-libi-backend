from django.urls import path

from .apps import LibiAccountConfig
from .views import (
    AccountRootView,
)

app_name = LibiAccountConfig.name

urlpatterns = [
    path('', AccountRootView.as_view(), name='account_root'),
]
