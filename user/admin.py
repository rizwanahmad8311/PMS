from django.contrib import admin
from user.models import User, ModulePermission


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "role", "status"]


@admin.register(ModulePermission)
class ModulePermissionAdmin(admin.ModelAdmin):
    list_display = ["id", "module"]
