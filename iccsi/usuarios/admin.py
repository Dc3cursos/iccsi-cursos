from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, DenunciaFalsificacion

class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Rol', {'fields': ('rol',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Rol', {'fields': ('rol',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'rol', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('rol', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    # Acciones personalizadas
    actions = ['make_professor', 'make_student', 'activate_users', 'deactivate_users']
    
    def make_professor(self, request, queryset):
        updated = queryset.update(rol='profesor')
        self.message_user(request, f'{updated} usuarios marcados como profesores.')
    make_professor.short_description = "Marcar como profesores"
    
    def make_student(self, request, queryset):
        updated = queryset.update(rol='alumno')
        self.message_user(request, f'{updated} usuarios marcados como alumnos.')
    make_student.short_description = "Marcar como alumnos"
    
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} usuarios activados.')
    activate_users.short_description = "Activar usuarios"
    
    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} usuarios desactivados.')
    deactivate_users.short_description = "Desactivar usuarios"

admin.site.register(Usuario, UsuarioAdmin)

@admin.register(DenunciaFalsificacion)
class DenunciaFalsificacionAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre_denunciante', 'tipo_denuncia', 'estado', 'fecha_denuncia']
    list_filter = ['estado', 'tipo_denuncia', 'fecha_denuncia', 'denuncia_anonima']
    search_fields = ['nombre_denunciante', 'email_denunciante', 'descripcion', 'folio_certificado']
    readonly_fields = ['fecha_denuncia', 'fecha_actualizacion']
    fieldsets = (
        ('Información del Denunciante', {
            'fields': ('nombre_denunciante', 'email_denunciante', 'telefono', 'denuncia_anonima')
        }),
        ('Detalles de la Denuncia', {
            'fields': ('tipo_denuncia', 'descripcion', 'folio_certificado', 'codigo_verificacion')
        }),
        ('Información del Incidente', {
            'fields': ('ubicacion', 'fecha_incidente', 'evidencia')
        }),
        ('Estado y Seguimiento', {
            'fields': ('estado', 'notas_internas', 'accion_tomada', 'fecha_accion', 'procesado_por')
        }),
        ('Información del Sistema', {
            'fields': ('fecha_denuncia', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('procesado_por')
