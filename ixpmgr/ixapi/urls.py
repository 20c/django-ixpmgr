"""ixpmgr URL Configuration

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
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls import handler404
from django.contrib import admin
from django.views.static import serve as serve_static

from rest_framework import routers

from . import views, errors

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"accounts", views.AccountViewSet)
router.register(r"facilities", views.FacilityViewSet)

# Pass basename to the endpoints with polymorphic serializers, DRF can't infer it
router.register(r"member-joining-rules", views.MemberJoiningRuleViewSet, basename='member-joining-rules')
router.register(r"network-services", views.NetworkServiceViewSet, basename='network-services')
router.register(r"network-service-configs", views.NetworkServiceConfigViewSet, basename='network-service-configs')
router.register(r"network-features", views.NetworkFeatureViewSet, basename='network-features')
router.register(r"ips", views.IpAddressViewSet, basename='ips')
router.register(r"macs", views.MacAddressViewSet, basename='macs')
router.register(r"connections", views.ConnectionViewSet, basename='connections')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v2/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    re_path(r'^static/(?P<path>.*)$', serve_static, {"document_root": settings.STATIC_ROOT}),
]

# only works if DEBUG=False
handler404 = errors.generic404
