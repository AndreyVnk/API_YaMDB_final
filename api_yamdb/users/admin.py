from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'role',
        'is_active',
        'is_staff',
    )
    ordering = ('username',)


admin.site.register(CustomUser, CustomUserAdmin)
