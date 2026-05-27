
from django.contrib import admin
from django.urls import path,include
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
#from drf_spectacular.views import SpectacularSwaggerView
from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
#from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
schema_view = get_schema_view(
    openapi.Info(
        title="Episyche Technologies",
        default_version='v1',),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
class HelloWorldView(APIView):
    @extend_schema(
        summary="Hello World",
        description="A simple API to return a Hello World message.",
        responses={200: dict},
    )
    def get(self, request):
        return Response({"message": "Hello, World!"})
urlpatterns = [
    path('admin/', admin.site.urls),
    # API Schema
    path('api/v1/captcha/', include('captcha.urls')),
    path('api/v1/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)