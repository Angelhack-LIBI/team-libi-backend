from django.urls import path

from ainize_api.views import DockerWebhookView
from libi_account.apps import LibiAccountConfig

app_name = LibiAccountConfig.name

urlpatterns = [
    path('', DockerWebhookView.as_view(), name='docker-webhook'),
]
