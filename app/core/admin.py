from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext

from core import models


# Register your models here.
# TODO: Change this view
class UserAdmin(UserAdmin):
    ordering = ['id']
    list_display = ['email', 'full_name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (gettext('Personal Info'), {'fields': ('full_name',)}),
        (
            gettext('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (gettext('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Product)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
