from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers

# from .views import (
#     # CustomerListAPIView,
#     CustomerViewSet,
#     RegularBinViewSet,
#     RegularShelfViewSet,
#     BinderViewSet,
# )
from . import views


# router = routers.DefaultRouter()
# router.register(r'customers', CustomerViewSet)
# router.register(r'bins', RegularBinViewSet)
# router.register(r'shelves', RegularShelfViewSet)
# router.register(r'binder', BinderViewSet)


urlpatterns = [
    # url(r'^', include(router.urls)),
    # url(r'^$', CustomerListAPIView.as_view(), name='list')

    url(r'^$', views.shelves_root),
    url(r'^shelves/$', views.RegularShelfList.as_view(),
        name="regularshelf-list"),
    url(r'^shelves/(?P<pk>[0-9]+)/$', views.RegularShelfDetail.as_view(),
        name="regularshelf-detail"),
    url(r'^customers/$', views.CustomerList.as_view(), name="customer-list"),
    url(r'^customers/(?P<pk>[0-9]+)/$', views.CustomerDetail.as_view(),
        name="customer-detail"),

    url(r'^users/$', views.UserList.as_view(), name="user-list"),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(),
        name="user-detail"),

]
