from django.contrib import admin
from django.utils.text import slugify
from django.utils.translation import ugettext as _

from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register)

from .models import Customer, RegularShelf, RegularBin, Binder, Upload


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("code", "user")


admin.site.register(Customer, CustomerAdmin)


class RegularShelfAdmin(admin.ModelAdmin):

    def get_size(self, obj):
        return "{}x{}".format(obj.cols, obj.rows)

    get_size.short_description = _("Size (colsxrows)")
    get_size.empty_value_display = '?'

    list_display = ('name', 'get_size')


admin.site.register(RegularShelf, RegularShelfAdmin)


class RegularBinAdmin(admin.ModelAdmin):
    list_display = ("id", "coordinate", "shelf")
    readonly_fields = ('coordinate', )
    # prepopulated_fields = {"coordinate": ("row", "col",)}


admin.site.register(RegularBin, RegularBinAdmin)


class BinderAdmin(admin.ModelAdmin):
    search_fields = ('biography__name', 'biography__code')

    def get_biography_code(self, obj):
        return obj.biography.code

    get_biography_code.short_description = _('Customer code')
    list_display = ("biography", "get_biography_code", "regular_bin")


admin.site.register(Binder, BinderAdmin)


class UploadAdmin(admin.ModelAdmin):
    list_display = ("csv_file", )


admin.site.register(Upload, UploadAdmin)


class CustomerWagtailAdmin(ModelAdmin):
    model = Customer
    # menu_label = _('Customer')
    list_display = ('user', 'code')
    list_filter = ('user', 'code')
    search_fields = ('user', 'code')
    menu_icon = 'group'


class RegularShelfWagtailAdmin(ModelAdmin):
    model = RegularShelf
    list_display = ('name', 'cols', 'rows')
    menu_icon = 'table'


class RegularBinWagtailAdmin(ModelAdmin):
    model = RegularBin
    # menu_label = _('Bin')
    list_filter = ('shelf', )
    list_display = ('shelf', 'coordinate')
    menu_icon = 'placeholder'


class BinderWagtailAdmin(ModelAdmin):
    model = Binder
    # menu_label = _('Binder')
    list_display = ('biography', 'regular_bin')
    list_filter = ('biography',)
    search_fields = ('biography', )
    menu_icon = 'folder-open-1'


class UploadWagtailAdmin(ModelAdmin):
    model = Upload
    menu_icon = 'order-up'


class ShelvesWagtailAdminGroup(ModelAdminGroup):
    items = (
        CustomerWagtailAdmin,
        RegularShelfWagtailAdmin,
        RegularBinWagtailAdmin,
        BinderWagtailAdmin,
        UploadWagtailAdmin)
    menu_icon = 'table'


modeladmin_register(ShelvesWagtailAdminGroup)
