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

    url(r'^binders/$', views.BinderViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name="binder-list"),
    url(r'^binders/(?P<pk>[0-9]+)/$', views.BinderViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    }), name="binder-detail"),

    url(r'^containers/$', views.ContainerList.as_view(),
        name="container-list"),
    url(r'^containers/(?P<pk>[0-9]+)/$', views.ContainerDetail.as_view(),
        name="container-detail"),

    url(r'^shelves/$', views.ShelfList.as_view(),
        name="shelf-list"),
    url(r'^shelves/(?P<pk>[0-9]+)/$', views.ShelfDetail.as_view(),
        name="shelf-detail"),
]
