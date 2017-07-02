from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers

from .views import (
    # CustomerListAPIView,
    CustomerViewSet,
)


router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^$', CustomerListAPIView.as_view(), name='list')
]
