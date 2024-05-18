from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="tickets Api V1",
        default_version='v1',
        description="Project built by osw4l",
        contact=openapi.Contact(email="ioswxd@gmail.com"),
        license=openapi.License(name="XD License"),
    ),
    public=True,
    permission_classes=[
        permissions.AllowAny,
    ],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('auth/', include('djoser.urls.authtoken')),
    path('tickets/', include('apps.tickets.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
