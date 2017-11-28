from django.contrib import admin
from django.utils.text import slugify
from django.utils.translation import ugettext as _

from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register)

from .models import (
    Customer,
    Shelf,
    Container,
    Binder,
    Upload)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name", "author")  # `name` previusly `user`

    fieldsets = [
        (None, {'fields': [('code', 'name')]}),
    ]

    def save_model(self, request, obj, form, change):
        """Save author as current user."""
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('name', 'desc',)
        }),
        ('Size options', {
            'classes': ('wide',),
            'description': _(
                "This option can be used for regular shelves."),
            'fields': (('cols', 'rows'), ),
        }),
        ('Number options', {
            'classes': ('wide',),
            'description': _(
                "This option can be used for irregular shelves. "),
            'fields': ('nums', ),
        }),
    )

    def save_model(self, request, obj, form, change):
        """Save author as current user."""
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()

    def view_size(self, obj):
        if obj.cols and obj.rows:
            return "{}x{}".format(obj.cols, obj.rows)

    view_size.short_description = _("Size (colsxrows)")
    view_size.empty_value_display = '-'

    list_display = ('id', 'name', 'desc', 'view_size', 'nums', 'author')

    def get_readonly_fields(self, request, obj=None):
        """Define readonly fields.

        Make dimensional fields readonly so the shelf cannot change size once
        it is defined.
        """
        if obj is None:
            return []
        return ['cols', 'rows', 'nums']


@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    list_display = ('id', 'shelf', 'col', 'row')
    readonly_fields = ('shelf', 'col', 'row')
    fields = ('shelf', ('col', 'row'))
    # prepopulated_fields = {'jsoncoord': ('col', 'row',)}

    # https://stackoverflow.com/questions/4043843/
    def has_delete_permission(self, request, obj=None):
        """Disable the delete link."""
        return False


@admin.register(Binder)
class BinderAdmin(admin.ModelAdmin):
    # search_fields = ('title', 'customer__code', 'customer__user__username')
    search_fields = ('title', 'customer__code', 'customer__name')

    def get_customer_code(self, obj):
        if obj.customer:
            return obj.customer.code

    get_customer_code.short_description = _('Customer code')
    list_display = ('id', 'title', 'customer', 'get_customer_code', 'container')
    list_filter = ('customer', 'container__shelf__name')


@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display = ("csv_file", )


class CustomerWagtailAdmin(ModelAdmin):
    model = Customer
    # menu_label = _('Customer')
    list_display = ('name', 'code')  # `name` previusly `user`
    list_filter = ('name', 'code')  # `name` previusly `user`
    search_fields = ('name', 'code')  # `name` previusly `user`
    menu_icon = 'group'


class ShelfWagtailAdmin(ModelAdmin):
    model = Shelf
    list_display = ('name', 'cols', 'rows')
    menu_icon = 'table'


class BinderWagtailAdmin(ModelAdmin):
    model = Binder
    # menu_label = _('Binder')
    list_display = ('customer', 'container')
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
        BinderWagtailAdmin,
        UploadWagtailAdmin)
    menu_icon = 'table'


modeladmin_register(ShelvesWagtailAdminGroup)
