from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.choose_contract, name='choose_contract'),
]
