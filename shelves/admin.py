from django.contrib import admin
from django.utils.text import slugify
from django.utils.translation import ugettext as _

from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register)

from .models import Customer, Shelf, Bin, Container, Binder, Upload


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("code", "user")


@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):

    fields = ('name', 'desc', ('cols', 'rows'), 'nums')

    def view_size(self, obj):
        if obj.cols and obj.rows:
            return "{}x{}".format(obj.cols, obj.rows)

    view_size.short_description = _("Size (colsxrows)")
    view_size.empty_value_display = '???'

    list_display = ('name', 'desc', 'view_size', 'nums', 'id')

    def get_readonly_fields(self, request, obj=None):
        """Define readonly fields.

        The shelf cannot change size once it is defined.
        """
        if obj is None:
            return []
        return ['cols', 'rows', 'nums']


@admin.register(Bin)
class BinAdmin(admin.ModelAdmin):
    list_display = ('id', 'shelf', 'row', 'col')
    readonly_fields = ('shelf', 'row', 'col')
    # prepopulated_fields = {'coordinate': ('row', 'col',)}

    fields = ('shelf', 'row', 'col')

    # https://stackoverflow.com/questions/4043843/
    def has_delete_permission(self, request, obj=None):
        """Disable the delete link."""
        return False


@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    list_display = ('id', 'shelf', 'num')
    readonly_fields = ('shelf', 'num')

    fields = ('shelf', 'num')

    # https://stackoverflow.com/questions/4043843/
    def has_delete_permission(self, request, obj=None):
        """Disable the delete link."""
        return False


@admin.register(Binder)
class BinderAdmin(admin.ModelAdmin):
    search_fields = ('customer__name', 'customer__code')

    def get_customer_code(self, obj):
        return obj.customer.code

    get_customer_code.short_description = _('Customer code')
    list_display = ('customer', 'get_customer_code', 'bin')


@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display = ("csv_file", )


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
    list_display = ('id', 'shelf', 'row', 'col')
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
