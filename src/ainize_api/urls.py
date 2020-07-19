from django.urls import path

from ainize_api.views import DockerWebhookView
from .apps import AinizeApiConfig

app_name = AinizeApiConfig.name

urlpatterns = [
    path('', DockerWebhookView.as_view(), name='docker-webhook'),
]
