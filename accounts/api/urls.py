from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.accounts_root),

    # url(r'^login/$', views.UserLoginAPIView.as_view(), name='login'),
    url(r'^register/$', views.MemberCreateAPIView.as_view(), name='register'),

    url(r'^users/$', views.UserList.as_view(), name="user-list"),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(),
        name="user-detail"),

    url(r'^members/$', views.MemberList.as_view(), name="member-list"),
    url(r'^members/(?P<pk>[0-9]+)/$', views.MemberDetail.as_view(),
        name="member-detail"),
]
