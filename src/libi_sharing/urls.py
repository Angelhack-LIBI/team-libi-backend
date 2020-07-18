from django.urls import path

from .apps import LibiSharingConfig
from .views import (
    SharingRootView,
    MyAreaView,
    CategoryView,
)

app_name = LibiSharingConfig.name

"""
쉐어링 등록
쉐어링 상세
쉐어링 참여
쉐어링 연락처
"""
urlpatterns = [
    path('', SharingRootView.as_view(), name='sharing'),
    path('area/me', MyAreaView.as_view(), name='my_area'),
    path('category', CategoryView.as_view(), name='category'),
]
