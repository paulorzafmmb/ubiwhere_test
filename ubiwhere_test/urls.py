# -*- coding: utf-8 -*-
# @Author: Paulo Barbosa
# @Date:   2025-05-28 21:16:06
# @Last Modified by:   Paulo Barbosa
# @Last Modified time: 2025-05-31 00:49:29

from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from traffic.views import RoadSegmentViewSet, RoadSpeedViewSet, CarViewSet, SensorViewSet, SensorReadingsViewSet

schema_view = get_schema_view(
    openapi.Info(
        title='Ubiwhere Test',
        default_version='v1',
        description="API docs for Traffic Statistics",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],
)

router = DefaultRouter()
router.register(r'segments', RoadSegmentViewSet)
router.register(r'speed', RoadSpeedViewSet)
router.register(r'car', CarViewSet)
router.register(r'sensor', SensorViewSet)
router.register(r'sensor_readings', SensorReadingsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)