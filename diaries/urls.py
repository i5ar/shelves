from django.conf.urls import url
from .views import DiariesView, EventList, CalendarList, RuleList

urlpatterns = [
    url(r'^$', DiariesView.as_view(), name="index"),
    url(r'^calendars/$', CalendarList.as_view(), name="calendars"),
    url(r'^events/$', EventList.as_view(), name="events"),
    url(r'^rules/$', RuleList.as_view(), name="rules"),
]
