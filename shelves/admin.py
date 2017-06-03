from django.contrib import admin
from django.utils.text import slugify
from django.utils.translation import ugettext as _

from . import models


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("code", "name")

admin.site.register(models.Customer, CustomerAdmin)


class RegularShelfAdmin(admin.ModelAdmin):

    def get_size(self, obj):
        return "{}x{}".format(obj.cols, obj.rows)

    get_size.short_description = _("Size (colsxrows)")
    get_size.empty_value_display = '?'

    list_display = ('name', 'get_size')

admin.site.register(models.RegularShelf, RegularShelfAdmin)

class RegularBinAdmin(admin.ModelAdmin):
    list_display = ("id", "coordinate", "shelf")
    readonly_fields=('coordinate', )
    # prepopulated_fields = {"coordinate": ("row", "col",)}

admin.site.register(models.RegularBin, RegularBinAdmin)


class BinderAdmin(admin.ModelAdmin):
    search_fields = ('biography__name', 'biography__code')

    def get_biography_code(self, obj):
        return obj.biography.code

    get_biography_code.short_description = _('Customer code')
    list_display = ("biography", "get_biography_code", "regular_bin")


admin.site.register(models.Binder, BinderAdmin)


class UploadAdmin(admin.ModelAdmin):
    list_display = ("csv_file", )

admin.site.register(models.Upload, UploadAdmin)
