from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.shelves_root),

    url(r'^users/$', views.UserList.as_view(), name='users-api'),
    url(
        r'^users/(?P<pk>[0-9]+)/$',
        views.UserRetrieve.as_view(),
        name='users_detail-api'
    ),

    url(
        r'^customers/$',
        views.CustomerListCreate.as_view(),
        name='customers-api'
    ),
    url(
        r'^customers/(?P<code>[-\w]+)/$',
        views.CustomerRetrieveUpdateDestroy.as_view(),
        name='customers_detail-api'
    ),

    url(r'^binders/$', views.BinderViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='binders-api'),
    url(r'^binders/(?P<pk>[0-9]+)/$', views.BinderViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    }), name='binders_detail-api'),

    url(r'^shelves/$', views.ShelfListCreate.as_view(), name='shelves-api'),
    url(
        r'^shelves/(?P<code>[-\w]+)/$',
        views.ShelfRetrieveUpdateDestroy.as_view(),
        name='shelves_detail-api'
    ),

    url(r'^uploads/$', views.UploadView.as_view(), name="uploads-api")
]
