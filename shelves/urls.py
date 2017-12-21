from django.conf.urls import url
from .views import import_data, BinderListView, BinderDetailView


urlpatterns = [
    url(r'^$', import_data, name='index'),
    url(r'^binders/$', BinderListView.as_view(), name="binders"),
    url(
        r'^binders/(?P<pk>\d+)/$',
        BinderDetailView.as_view(),
        name='binders-detail'
    ),
]
