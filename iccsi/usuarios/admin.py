from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Rol', {'fields': ('rol',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Rol', {'fields': ('rol',)}),
    )
    list_display = UserAdmin.list_display + ('email', 'rol', 'is_staff', 'is_active', 'date_joined')
    list_filter = UserAdmin.list_filter + ('rol', 'is_staff', 'is_active')
    search_fields = UserAdmin.search_fields + ('email', 'username')

admin.site.register(Usuario, UsuarioAdmin)
