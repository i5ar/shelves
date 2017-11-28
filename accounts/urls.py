from django.conf.urls import url

from .views import index, edit, edit_user, edit_member, edit_biography, detail

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^edit/$', edit, name='edit'),
    url(r'^edit/user/$', edit_user, name='edit-user'),
    url(r'^edit/member/$', edit_member, name='edit-member'),
    url(r'^edit/biography/$', edit_biography, name='edit-biography'),
    url(r'^detail/(?P<username>[a-zA-Z0-9]+)/$', detail, name='detail'),
]
