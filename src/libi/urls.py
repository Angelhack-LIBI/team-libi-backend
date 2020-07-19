"""libi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import ainize_api.urls as ainize_api_urls
import libi_account.urls as account_urls
import libi_sharing.urls as sharing_urls
from libi_common.meta_views import api_document

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include(account_urls, namespace='account_v1')),
    path('sharing/', include(sharing_urls, namespace='sharing_v1')),
    path('docs/', api_document()),
    path('api/ainize/', include(ainize_api_urls, namespace='ainize_api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
