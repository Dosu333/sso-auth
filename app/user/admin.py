from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import User, Token


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('id', 'firstname', 'lastname', 'email', 'phone', 'verified', 'password', 'roles', 'is_active',
                  'is_staff', 'is_superuser', 'referred_by', 'referred_by_hero', 'referred_by_store_owner')


class UserAdmin(BaseUserAdmin, ImportExportModelAdmin):
    resource_class = UserResource

    ordering = ['email']
    list_display = ['email', 'lastname', 'firstname',
                    'roles', 'verified', 'created_at']
    list_filter = ['is_active', 'is_staff', 'verified']
    search_fields = ('id', 'email', 'lastname', 'firstname', 'phone', 'roles')
    date_hierarchy = 'created_at'
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {
            'fields': ('lastname', 'firstname', 'phone', 'roles', 'image', 'businessname', 'address', 'state')}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser', 'verified',
                        'referred_by', 'referred_by_hero', 'referred_by_store_owner')}
        ),
        (_('Important Info'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'lastname', 'firstname', 'roles', 'verified', 'password1', 'password2')
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Token)
