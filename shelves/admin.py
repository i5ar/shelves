import csv

from django.contrib import admin
from django.utils.translation import ugettext as _
from django.core.files.storage import default_storage
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from django import forms

from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register
)

from .models import (
    Customer,
    Shelf,
    Binder,
    Upload,
    Attachment,
)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "code",
        "name",
        "get_binder_id",
        "get_author_username",
    )
    prepopulated_fields = {"code": ("name",)}

    def get_binder_id(self, obj):
        binder = Binder.objects.get(customer=obj)
        if binder.id:
            return "{}".format(binder.id)

    get_binder_id.short_description = _("Binder id")

    def get_author_username(self, obj):
        return obj.author.username

    get_author_username.short_description = _('Author username')

    # NOTE: Hide author selection and save author as current user.
    def get_readonly_fields(self, request, obj=None):
        """Make ``author`` field readonly for regular users on update."""
        return ['author'] if obj and not request.user.is_superuser else []

    def get_form(self, request, obj=None, **kwargs):
        """Hide ``author`` selection default to request user on create."""
        form = super().get_form(request, obj, **kwargs)
        if not obj:
            form.base_fields['author'].initial = request.user
        if not obj and not request.user.is_superuser:
            form.base_fields['author'].widget = forms.HiddenInput()
        return form

    def save_model(self, request, obj, form, change):
        """Save ``author`` field as request user to prevent hack on create."""
        if getattr(obj, 'author') != request.user and not change:
            if not request.user.is_superuser:
                obj.author = request.user
        super().save_model(request, obj, form, change)

    list_filter = ('author',)


@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('name', 'code', 'desc', 'author')
        }),
        ('Size options', {
            'classes': ('wide',),
            'description': _("Shelf size."),
            'fields': (('cols', 'rows'), ),
        }),
    )
    prepopulated_fields = {"code": ("name",)}

    def view_size(self, obj):
        if obj.cols and obj.rows:
            return "{}*{}".format(obj.cols, obj.rows)

    view_size.short_description = _("Size")
    view_size.empty_value_display = '-'

    list_display = (
        'id',
        'code',
        'name',
        'desc',
        'view_size',
        'get_author_username',
    )

    def get_author_username(self, obj):
        return obj.author.username

    get_author_username.short_description = _('Author username')

    def get_readonly_fields(self, request, obj=None):
        """Make ``author`` field and dimensional fields readonly."""
        if obj and request.user.is_superuser:
            return ['cols', 'rows']
        elif obj and not request.user.is_superuser:
            return ['cols', 'rows', 'author']
        else:
            return []

    # NOTE: Hide author selection and save author as current user.
    def get_form(self, request, obj=None, **kwargs):
        """Hide ``author`` selection default to request user on create."""
        form = super().get_form(request, obj, **kwargs)
        if not obj:
            form.base_fields['author'].initial = request.user
        if not obj and not request.user.is_superuser:
            form.base_fields['author'].widget = forms.HiddenInput()
        return form

    def save_model(self, request, obj, form, change):
        """Save ``author`` field as request user to prevent hack on create."""
        if getattr(obj, 'author') != request.user and not change:
            if not request.user.is_superuser:
                obj.author = request.user
        super().save_model(request, obj, form, change)


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1


@admin.register(Binder)
class BinderAdmin(admin.ModelAdmin):
    search_fields = (
        'title',
        'content',
        'customer__code',
        'customer__name',
    )

    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'customer', 'color')
        }),
        ('Position', {
            'classes': ('wide',),
            'description': _("Position in the shelf."),
            'fields': (('col', 'row', 'shelf',),),
        }),
    )

    inlines = [AttachmentInline]

    def view_coord(self, obj):
        if obj.col and obj.row:
            return "[{}, {}]".format(obj.col, obj.row)

    view_coord.short_description = _("Coordinate")
    view_coord.empty_value_display = '-'

    def get_customer_name(self, obj):
        if obj.customer:
            return obj.customer.name

    def get_customer_code(self, obj):
        if obj.customer:
            return obj.customer.code

    def get_shelf_id(self, obj):
        if obj.shelf:
            return obj.shelf.id

    get_customer_code.short_description = _('Customer code')
    get_customer_name.short_description = _('Customer name')
    get_shelf_id.short_description = _('Shelf')

    list_display = (
        'id',
        'title',
        'updated',
        'view_coord',
        'customer',
        'get_customer_code',
        'get_customer_name',
        'get_shelf_id')

    list_filter = ('customer', 'shelf__name')


@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display = ("csv_file", )

    def save_model(self, request, obj, form, change):
        """Create customers from a CSV file.

        .. _Save model:
            https://docs.djangoproject.com/en/2.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.save_model

        """
        super().save_model(request, obj, form, change)

        # Import CSV data
        # http://stackoverflow.com/questions/2459979/
        with open(default_storage.path(obj.csv_file)) as f:
            has_header = csv.Sniffer().has_header(f.read(1024))
            f.seek(0)
            if has_header:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        Customer.objects.get_or_create(
                            name=row['name'],
                            code=row['code'],
                            note=row['note'],
                            author=request.user
                        )
                    except IntegrityError as e:
                        """
                        An integrity error may happen if two customers have the
                        same code.
                        """
                        # print('{0!r}'.format(e))
                        raise ValidationError(e, code='integrity')
                    except KeyError as e:
                        """
                        Key error may happen if CSV header is divergent
                        from model fields
                        """
                        try:
                            """
                            Pretend internationalized field name match the
                            CSV header
                            """
                            Customer.objects.get_or_create(
                                name=row[_('name')],
                                code=row[_('code')],
                                note=row[_('note')],
                                author=request.user
                            )
                        except KeyError as e:
                            raise ValidationError(
                                'Is the field {} present in the CSV file '
                                'header?'.format(e),
                                code='key'
                            )

            else:
                raise ValidationError(
                    _(
                        'The CSV file require a proper header in order.'
                        'Be sure to provide an id field.'
                    ), code='invalid'
                )
