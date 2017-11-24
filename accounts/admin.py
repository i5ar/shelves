from django.contrib import admin

from .models import Membership, Biography


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'membership')


@admin.register(Biography)
class BiographyAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'gender_visible')
