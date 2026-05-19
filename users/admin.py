from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'is_staff']
    list_filter = ['role']
    fieldsets = UserAdmin.fieldsets + (
        ('Job Portal Info', {'fields': ('role', 'skills', 'bio')}),
    )