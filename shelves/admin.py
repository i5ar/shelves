from django.contrib import admin
from django.utils.text import slugify

from . import models


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("codice", "nome")

admin.site.register(models.Customer, CustomerAdmin)


class ShelfAdmin(admin.ModelAdmin):
    list_display = ("name", )

admin.site.register(models.Shelf, ShelfAdmin)


class BinAdmin(admin.ModelAdmin):
    list_display = ("id", "coordinate")
    readonly_fields=('coordinate', )
    # prepopulated_fields = {"coordinate": ("row", "col",)}

admin.site.register(models.Bin, BinAdmin)


class BinderAdmin(admin.ModelAdmin):
    search_fields = ('biography__nome', 'biography__codice')

    def get_biography_code(self, obj):
        return obj.biography.codice

    get_biography_code.short_description = 'codice cliente'
    list_display = ("biography", "get_biography_code", "shelf", "shelf_bin")


admin.site.register(models.Binder, BinderAdmin)


class UploadAdmin(admin.ModelAdmin):
    list_display = ("csv_file", )

admin.site.register(models.Upload, UploadAdmin)
