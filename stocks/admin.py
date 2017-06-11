from django.contrib import admin
from django.utils.translation import ugettext as _

# Register your models here.
from .models import Dispatched, Approved
# from django.contrib.auth.models import User

class DispatchedAdmin(admin.ModelAdmin):
    """Customize the look of the auto-generated admin for the DispatchedCertification model"""
    list_display = ('code', 'dispatch')
    list_filter = ('customer', )
    readonly_fields=('stock_year_customer', )

# admin.site.register(User)  # Use the default options
admin.site.register(Dispatched, DispatchedAdmin)  # Use the customized options


class ApprovedAdmin(admin.ModelAdmin):
    """Customize the look of the auto-generated admin for the DispatchedCertification model"""
    list_display = ('dispatched', 'approval')
    list_filter = ('dispatched', )

admin.site.register(Approved, ApprovedAdmin)  # Use the customized options


# Wagtail
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register)


class DispatchedWagtailAdmin(ModelAdmin):
    model = Dispatched
    list_display = ('code', 'dispatch')
    list_filter = ('code', 'dispatch')
    search_fields = ('code', 'dispatch')
    menu_icon = 'placeholder'


class ApprovedWagtailAdmin(ModelAdmin):
    model = Approved
    list_display = ('dispatched', 'approval')
    menu_icon = 'tick-inverse'


class StocksWagtailAdminGroup(ModelAdminGroup):
    items = (
        DispatchedWagtailAdmin,
        ApprovedWagtailAdmin)
    menu_icon = 'doc-full-inverse'

modeladmin_register(StocksWagtailAdminGroup)
