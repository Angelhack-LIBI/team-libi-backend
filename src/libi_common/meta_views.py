from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny


def api_document():
    schema_view = get_schema_view(
        openapi.Info(
            title="LIBI API",
            default_version="v1",
            description="AngelHack 2020 LIBI API",
            contact=openapi.Contact(email="kde713@gmail.com"),
        ),
        public=True,
        permission_classes=(AllowAny,),
    )
    return schema_view.with_ui('redoc', cache_timeout=0)
