from django.db import models
from django.conf import settings

class Organizacion(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.nombre


class Curso(models.Model):
    # Se amplía a 255 para permitir títulos extensos del catálogo
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    duracion_horas = models.PositiveSmallIntegerField(null=True, blank=True)
    profesor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cursos_creados'
    )
    organizacion = models.ForeignKey(
        Organizacion,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='cursos/imagenes/', null=True, blank=True)
    video = models.FileField(upload_to='cursos/videos/', null=True, blank=True)

    class Meta:
        unique_together = ('nombre', 'organizacion')

    def __str__(self):
        return self.nombre


class Inscripcion(models.Model):
    alumno = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='inscripciones'
    )
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name='inscripciones'
    )
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('alumno', 'curso')

    def __str__(self):
        return f"{self.alumno.username} en {self.curso.nombre}"


class Empresa(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    rfc = models.CharField(max_length=13, unique=True)
    representante_legal = models.CharField(max_length=200)
    representante_trabajadores = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.nombre} ({self.rfc})"

class CertificadoDC3(models.Model):
    inscripcion = models.OneToOneField('Inscripcion', on_delete=models.CASCADE, related_name='certificado')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)
    # Nuevos campos separados para el nombre del trabajador
    apellido_paterno = models.CharField(max_length=100, null=True, blank=True)
    apellido_materno = models.CharField(max_length=100, null=True, blank=True)
    nombres = models.CharField(max_length=200, null=True, blank=True)
    # Campo legado para compatibilidad; se mantendrá como respaldo
    nombre_completo = models.CharField(max_length=200, null=True, blank=True)
    curp = models.CharField(max_length=18)
    puesto = models.CharField(max_length=100)
    horas_curso = models.PositiveSmallIntegerField()
    fecha_emision = models.DateField(auto_now_add=True)
    # Campo para guardar el archivo PDF generado
    archivo_pdf = models.FileField(upload_to='certificados/dc3/', null=True, blank=True)

    def __str__(self):
        return f"DC-3 de {self.inscripcion.alumno.username} para {self.inscripcion.curso.nombre}"


class Recurso(models.Model):
    nombre = models.CharField(max_length=200)
    archivo = models.FileField(upload_to='cursos/recursos/', null=True, blank=True)
    enlace = models.URLField(null=True, blank=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='recursos')

    def __str__(self) -> str:
        return self.nombre


class PlantillaDC3(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    archivo = models.FileField(upload_to='plantillas/dc3/')
    organizacion = models.ForeignKey(Organizacion, null=True, blank=True, on_delete=models.SET_NULL)
    empresa = models.ForeignKey(Empresa, null=True, blank=True, on_delete=models.SET_NULL)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Plantilla DC-3'
        verbose_name_plural = 'Plantillas DC-3'

    def __str__(self) -> str:
        destino = self.organizacion or self.empresa or 'Genérica'
        return f"{self.nombre} ({destino})"


class LogoDC3(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    imagen = models.ImageField(upload_to='plantillas/logos/')
    organizacion = models.ForeignKey(Organizacion, null=True, blank=True, on_delete=models.SET_NULL)
    empresa = models.ForeignKey(Empresa, null=True, blank=True, on_delete=models.SET_NULL)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Logo DC-3'
        verbose_name_plural = 'Logos DC-3'

    def __str__(self) -> str:
        destino = self.organizacion or self.empresa or 'Genérico'
        return f"{self.nombre} ({destino})"


class HistorialCertificadoDC3(models.Model):
    """
    Modelo para llevar control y verificación de todos los certificados DC-3 generados
    """
    # Datos del alumno
    nombre_completo_alumno = models.CharField(max_length=300)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100) 
    nombres = models.CharField(max_length=200)
    curp = models.CharField(max_length=18)
    
    # Datos de la empresa
    nombre_empresa = models.CharField(max_length=200)
    rfc_empresa = models.CharField(max_length=13)
    
    # Datos del curso
    nombre_curso = models.CharField(max_length=255)
    horas_curso = models.PositiveSmallIntegerField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    
    # Datos del instructor
    instructor_nombre = models.CharField(max_length=200)
    
    # Control del certificado
    folio = models.CharField(max_length=20, null=True, blank=True)  # Folio único del certificado
    codigo_verificacion = models.CharField(max_length=12, unique=True)  # Código único de verificación
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    archivo_pdf_path = models.CharField(max_length=500, null=True, blank=True)  # Ruta del archivo PDF
    
    # Relación con inscripción original (si existe)
    inscripcion = models.ForeignKey(Inscripcion, on_delete=models.SET_NULL, null=True, blank=True, related_name='historial_certificados')
    
    # Usuario que generó el certificado
    generado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['folio']),
            models.Index(fields=['codigo_verificacion']),
            models.Index(fields=['nombre_completo_alumno', 'nombre_empresa']),
            models.Index(fields=['curp']),
        ]
        verbose_name = 'Historial Certificado DC-3'
        verbose_name_plural = 'Historial Certificados DC-3'
    
    def __str__(self):
        return f"DC-3: {self.nombre_completo_alumno} - {self.nombre_empresa} - {self.nombre_curso}"