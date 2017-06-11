from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, TemplateView
from schedule.models.events import Event
from schedule.models.calendars import Calendar
from schedule.models.rules import Rule


class DiariesView(TemplateView):
    template_name = "diaries/index.html"


class CalendarList(ListView):
    model = Calendar
    template_name = 'diaries/calendar_list.html'


class EventList(ListView):
    model = Event
    template_name = 'diaries/event_list.html'


class RuleList(ListView):
    model = Rule
    template_name = 'diaries/rule_list.html'
