from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from registration.admin import RegistrationAdmin
from registration.models import RegistrationProfile

from .models import Member, Biography


@admin.register(Member)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'membership')


@admin.register(Biography)
class BiographyAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'gender_visible')


# User model
# https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#extending-the-existing-user-model
# https://docs.djangoproject.com/en/1.8/ref/contrib/admin/#inlinemodeladmin-objects
class MembershipInline(admin.StackedInline):
    '''Add Member Model'''
    model = Member
    # can_delete = False
    verbose_name_plural = 'User membership'


# Customizing
# https://docs.djangoproject.com/en/1.8/topics/auth/customizing/
class MembershipUserAdmin(UserAdmin):
    '''Add Member lists to the Admin User Panel'''
    inlines = (MembershipInline, )
    list_display = UserAdmin.list_display + ('date_joined', 'get_membership')

    # Model Admin
    # https://docs.djangoproject.com/en/1.8/ref/contrib/admin/#modeladmin-options
    def get_membership(self, obj):
        '''Add User ID list to the Admin Registration Panel'''
        member = obj.member
        return member.membership

    # Allows HTML
    get_membership.allow_tags = True
    # Customize heading title in changelist
    get_membership.short_description = 'Membership'
    # Database field to order in relation to
    get_membership.admin_order_field = 'member'


admin.site.unregister(User)
admin.site.register(User, MembershipUserAdmin)
