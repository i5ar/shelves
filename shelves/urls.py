from django.conf.urls import url
from .views import import_data


urlpatterns = [
    url(r'^$', import_data, name='import_data'),
]
