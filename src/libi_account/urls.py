from django.urls import path

from .apps import LibiAccountConfig
from .views import (
    AccountView,
    TokenView,
)

app_name = LibiAccountConfig.name

urlpatterns = [
    path('', AccountView.as_view(), name='account'),
    path('token', TokenView.as_view(), name='token'),
]
