from django.contrib import admin
from django.utils.translation import ugettext as _

from schedule.models.events import Event
from schedule.models.calendars import Calendar
from schedule.models.rules import Rule


# Wagtail
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register)


class EventWagtailAdmin(ModelAdmin):
    model = Event
    list_display = ('title', 'start', 'end', 'creator', 'updated_on', 'calendar', 'rule')
    list_filter = ('start', 'creator', 'calendar')
    search_fields = ('title', )
    menu_icon = 'tag'


class CalendarWagtailAdmin(ModelAdmin):
    model = Calendar
    list_display = ('name', 'slug')
    menu_icon = 'date'


class RuleWagtailAdmin(ModelAdmin):
    model = Rule
    list_filter = ('frequency', )
    list_display = ('name', 'frequency')
    menu_icon = 'locked'


class DiariesWagtailAdminGroup(ModelAdminGroup):
    items = (
        EventWagtailAdmin,
        CalendarWagtailAdmin,
        RuleWagtailAdmin)
    menu_icon = 'date'

modeladmin_register(DiariesWagtailAdminGroup)
