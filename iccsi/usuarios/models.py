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