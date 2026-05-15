from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger / drf-yasg
schema_view = get_schema_view(
    openapi.Info(
        title="Evidencias API",
        default_version='v1',
        description="API para gestión de evidencias de proyectos con autenticación Google + JWT",
        contact=openapi.Contact(email="admin@example.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

def health_check(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path('admin/', admin.site.urls),

    # Health check
    path('health/', health_check, name='health'),

    # Apps
    path('api/auth/', include('auth_api.urls')),
    path('api/evidencias/', include('evidencias.urls')),

    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
]
