from django.contrib import admin
from django.utils.text import slugify
from django.utils.translation import ugettext as _

from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register)

from .models import Customer, Shelf, Bin, Binder, Upload


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("code", "user")


admin.site.register(Customer, CustomerAdmin)


class ShelfAdmin(admin.ModelAdmin):

    def get_size(self, obj):
        return "{}x{}".format(obj.cols, obj.rows)

    get_size.short_description = _("Size (colsxrows)")
    get_size.empty_value_display = '?'

    list_display = ('name', 'get_size')


admin.site.register(Shelf, ShelfAdmin)


class BinAdmin(admin.ModelAdmin):
    list_display = ("id", "coordinate", "shelf")
    readonly_fields = ('coordinate', )
    # prepopulated_fields = {"coordinate": ("row", "col",)}


admin.site.register(Bin, BinAdmin)


class BinderAdmin(admin.ModelAdmin):
    search_fields = ('customer__name', 'customer__code')

    def get_customer_code(self, obj):
        return obj.customer.code

    get_customer_code.short_description = _('Customer code')
    list_display = ("customer", "get_customer_code", "bin")


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


class ShelfWagtailAdmin(ModelAdmin):
    model = Shelf
    list_display = ('name', 'cols', 'rows')
    menu_icon = 'table'


class BinWagtailAdmin(ModelAdmin):
    model = Bin
    # menu_label = _('Bin')
    list_filter = ('shelf', )
    list_display = ('shelf', 'coordinate')
    menu_icon = 'placeholder'


class BinderWagtailAdmin(ModelAdmin):
    model = Binder
    # menu_label = _('Binder')
    list_display = ('customer', 'bin')
    list_filter = ('customer',)
    search_fields = ('customer', )
    menu_icon = 'folder-open-1'


class UploadWagtailAdmin(ModelAdmin):
    model = Upload
    menu_icon = 'order-up'


class ShelvesWagtailAdminGroup(ModelAdminGroup):
    items = (
        CustomerWagtailAdmin,
        ShelfWagtailAdmin,
        BinWagtailAdmin,
        BinderWagtailAdmin,
        UploadWagtailAdmin)
    menu_icon = 'table'


modeladmin_register(ShelvesWagtailAdminGroup)
