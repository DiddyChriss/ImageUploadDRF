from django.contrib import admin
from django.contrib.auth import get_user_model

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Plan, Image

from .forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('username',)
    list_filter = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password', 'plan')}),
        # ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2','plan','is_admin', 'is_admin', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.register(Plan)
admin.site.register(Image),

admin.site.unregister(Group)