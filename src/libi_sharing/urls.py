from django.urls import path

from .apps import LibiSharingConfig
from .views import (
    SharingRootView,
)

app_name = LibiSharingConfig.name

"""
메인 리스트
검색 필터
카테고리
쉐어링 등록
쉐어링 상세
쉐어링 참여
쉐어링 연락처
"""
urlpatterns = [
    path('', SharingRootView.as_view(), name='sharing'),
]
