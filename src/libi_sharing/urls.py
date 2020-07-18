from django.urls import path

from .apps import LibiSharingConfig
from .views import (
    SharingRootView,
    SharingItemView,
    SharingApplyView,
    SharingContactView,
    MyAreaView,
    CategoryView,
)

app_name = LibiSharingConfig.name

urlpatterns = [
    path('', SharingRootView.as_view(), name='sharing'),
    path('<int:sharing_id>', SharingItemView.as_view(), name='sharing_item'),
    path('<int:sharing_id>/apply', SharingApplyView.as_view(), name='sharing_apply'),
    path('<int:sharing_id>/contact', SharingContactView.as_view(), name='sharing_contact'),
    path('area/me', MyAreaView.as_view(), name='my_area'),
    path('category', CategoryView.as_view(), name='category'),
]
