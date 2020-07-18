from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers

from .apps import LibiSharingConfig
from .views import SharingView

app_name = LibiSharingConfig.name

router = routers.DefaultRouter()
router.register(r'', SharingView, basename='cutareadel')

urlpatterns = [
    url('', include(router.urls)),
]
