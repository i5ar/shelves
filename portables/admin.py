from django.contrib import admin
from django.utils.translation import ugettext as _

# Register your models here.
from .models import DownloadModel, ContractModel, LayoutModel, CompanyModel


class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "address")

admin.site.register(CompanyModel, CompanyAdmin)

admin.site.register(ContractModel)

class LayoutAdmin(admin.ModelAdmin):
    list_display = ("recipient", "tep", "trees", "contract")
    readonly_fields=('co2', 'trees')

admin.site.register(LayoutModel, LayoutAdmin)

class DownloadAdmin(admin.ModelAdmin):
    list_display = ("created", "name")

admin.site.register(DownloadModel, DownloadAdmin)


# Wagtail
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register)


class CompanyWagtailAdmin(ModelAdmin):
    model = CompanyModel
    list_display = ('name', 'address')
    list_filter = ('name', 'address')
    search_fields = ('name', 'address')
    menu_icon = 'group'


class ContractWagtailAdmin(ModelAdmin):
    model = ContractModel
    list_display = ('title', 'content', 'company')
    menu_icon = 'doc-empty'


class LayoutWagtailAdmin(ModelAdmin):
    model = LayoutModel
    list_filter = ('recipient', )
    list_display = ('recipient', 'tep', 'trees', 'contract')
    menu_icon = 'doc-full'


class DownloadWagtailAdmin(ModelAdmin):
    model = DownloadModel
    list_display = ('created', 'name')
    list_filter = ('created',)
    search_fields = ('created', )
    menu_icon = 'download'


class PortableWagtailAdminGroup(ModelAdminGroup):
    items = (
        CompanyWagtailAdmin,
        ContractWagtailAdmin,
        LayoutWagtailAdmin,
        DownloadWagtailAdmin)
    menu_icon = 'doc-full-inverse'

modeladmin_register(PortableWagtailAdminGroup)
