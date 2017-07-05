from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.shelves_root),

    url(r'^users/$', views.UserList.as_view(), name="user-list"),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(),
        name="user-detail"),

    url(r'^customers/$', views.CustomerList.as_view(), name="customer-list"),
    url(r'^customers/(?P<pk>[0-9]+)/$', views.CustomerDetail.as_view(),
        name="customer-detail"),

    url(r'^binders/$', views.BinderList.as_view(),
        name="binder-list"),
    url(r'^binders/(?P<pk>[0-9]+)/$', views.BinderDetail.as_view(),
        name="binder-detail"),

    url(r'^bins/$', views.BinList.as_view(),
        name="bin-list"),
    url(r'^bins/(?P<pk>[0-9]+)/$', views.BinDetail.as_view(),
        name="bin-detail"),

    url(r'^shelves/$', views.ShelfList.as_view(),
        name="shelf-list"),
    url(r'^shelves/(?P<pk>[0-9]+)/$', views.ShelfDetail.as_view(),
        name="shelf-detail"),
]
