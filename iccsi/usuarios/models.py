from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES = (
        ('alumno', 'Alumno'),
        ('profesor', 'Profesor'),
    )
    rol = models.CharField(max_length=10, choices=ROLES, default='alumno')

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"


class DenunciaFalsificacion(models.Model):
    """Modelo para almacenar denuncias de falsificación de certificados DC-3"""
    
    TIPO_DENUNCIA_CHOICES = [
        ('falsificacion', 'Certificado Falsificado'),
        ('alteracion', 'Certificado Alterado'),
        ('uso_fraudulento', 'Uso Fraudulento'),
        ('venta_ilegal', 'Venta Ilegal'),
        ('otro', 'Otro'),
    ]
    
    ESTADO_CHOICES = [
        ('recibida', 'Recibida'),
        ('en_revision', 'En Revisión'),
        ('validada', 'Validada'),
        ('enviada_autoridades', 'Enviada a Autoridades'),
        ('cerrada', 'Cerrada'),
        ('rechazada', 'Rechazada'),
    ]
    
    # Información del denunciante
    nombre_denunciante = models.CharField(max_length=200)
    email_denunciante = models.EmailField()
    telefono = models.CharField(max_length=15, blank=True, null=True)
    denuncia_anonima = models.BooleanField(default=False)
    
    # Información de la denuncia
    tipo_denuncia = models.CharField(max_length=20, choices=TIPO_DENUNCIA_CHOICES)
    descripcion = models.TextField()
    folio_certificado = models.CharField(max_length=50, blank=True, null=True)
    codigo_verificacion = models.CharField(max_length=20, blank=True, null=True)
    
    # Información del incidente
    ubicacion = models.CharField(max_length=200, blank=True, null=True)
    fecha_incidente = models.DateField(blank=True, null=True)
    
    # Evidencia
    evidencia = models.FileField(upload_to='denuncias/evidencia/', blank=True, null=True)
    
    # Estado y seguimiento
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='recibida')
    fecha_denuncia = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # Información de seguimiento
    notas_internas = models.TextField(blank=True, null=True)
    accion_tomada = models.TextField(blank=True, null=True)
    fecha_accion = models.DateTimeField(blank=True, null=True)
    
    # Usuario que procesa la denuncia (si está autenticado)
    procesado_por = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        related_name='denuncias_procesadas'
    )
    
    class Meta:
        verbose_name = 'Denuncia de Falsificación'
        verbose_name_plural = 'Denuncias de Falsificación'
        ordering = ['-fecha_denuncia']
    
    def __str__(self):
        return f"Denuncia {self.id} - {self.tipo_denuncia} - {self.fecha_denuncia.strftime('%d/%m/%Y')}"
    
    def get_estado_display_color(self):
        """Retorna el color CSS para el estado"""
        colores = {
            'recibida': 'primary',
            'en_revision': 'warning',
            'validada': 'info',
            'enviada_autoridades': 'danger',
            'cerrada': 'success',
            'rechazada': 'secondary',
        }
        return colores.get(self.estado, 'secondary')