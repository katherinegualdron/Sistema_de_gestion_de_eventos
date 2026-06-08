from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from api.auth_views import StandardTokenObtainPairView, StandardTokenRefreshView


swagger_patterns = [
    path('api/v1/token/', StandardTokenObtainPairView.as_view(), name='token_obtain_pair_v1_docs'),
    path('api/v1/token/refresh/', StandardTokenRefreshView.as_view(), name='token_refresh_v1_docs'),
    path('api/v1/', include('api.urls')),
]

api_v1_patterns = [
    path('', include('api.urls')),
]

schema_view = get_schema_view(
    openapi.Info(
        title='API Sistema de Gestion de Eventos',
        default_version='v1',
        description='Documentacion Swagger de la API CRUD para gestion de eventos.',
    ),
    url='http://127.0.0.1:8000',
    patterns=swagger_patterns,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/token/', StandardTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', StandardTokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/', StandardTokenObtainPairView.as_view(), name='token_obtain_pair_v1'),
    path('api/v1/token/refresh/', StandardTokenRefreshView.as_view(), name='token_refresh_v1'),
    path('api/<str:version>/', include(api_v1_patterns)),
    path('api/', include('api.urls')),
]
