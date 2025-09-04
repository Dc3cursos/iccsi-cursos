"""
Serializers para la API REST de ICCSI
"""
from rest_framework import serializers
from .models import (
    Curso, Organizacion, Inscripcion, CertificadoDC3, 
    PlantillaDC3, Empresa
)
from iccsi.usuarios.models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    """Serializer para usuarios"""
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'rol']
        read_only_fields = ['id']

class OrganizacionSerializer(serializers.ModelSerializer):
    """Serializer para organizaciones"""
    class Meta:
        model = Organizacion
        fields = ['id', 'nombre']

class EmpresaSerializer(serializers.ModelSerializer):
    """Serializer para empresas"""
    class Meta:
        model = Empresa
        fields = ['id', 'nombre', 'rfc', 'representante_legal', 'representante_trabajadores']

class CursoSerializer(serializers.ModelSerializer):
    """Serializer para cursos"""
    organizacion = OrganizacionSerializer(read_only=True)
    profesor = UsuarioSerializer(read_only=True)
    
    class Meta:
        model = Curso
        fields = [
            'id', 'nombre', 'descripcion', 'duracion_horas', 
            'organizacion', 'profesor', 'fecha_creacion', 'imagen', 'video'
        ]
        read_only_fields = ['id', 'fecha_creacion']

class InscripcionSerializer(serializers.ModelSerializer):
    """Serializer para inscripciones"""
    curso = CursoSerializer(read_only=True)
    alumno = UsuarioSerializer(read_only=True)
    
    class Meta:
        model = Inscripcion
        fields = ['id', 'curso', 'alumno', 'fecha_inscripcion']
        read_only_fields = ['id', 'fecha_inscripcion']

class PlantillaDC3Serializer(serializers.ModelSerializer):
    """Serializer para plantillas DC-3"""
    organizacion = OrganizacionSerializer(read_only=True)
    empresa = EmpresaSerializer(read_only=True)
    
    class Meta:
        model = PlantillaDC3
        fields = [
            'id', 'nombre', 'archivo', 'organizacion', 
            'empresa', 'activo', 'creado'
        ]
        read_only_fields = ['id', 'creado']

class CertificadoDC3Serializer(serializers.ModelSerializer):
    """Serializer para certificados DC-3"""
    inscripcion = InscripcionSerializer(read_only=True)
    empresa = EmpresaSerializer(read_only=True)
    
    class Meta:
        model = CertificadoDC3
        fields = [
            'id', 'inscripcion', 'empresa', 'apellido_paterno',
            'apellido_materno', 'nombres', 'curp', 'puesto',
            'horas_curso', 'fecha_emision', 'archivo_pdf'
        ]
        read_only_fields = ['id', 'fecha_emision']

class GenerarCertificadoSerializer(serializers.Serializer):
    """Serializer para generar certificados"""
    plantilla_id = serializers.IntegerField()
    apellido_paterno = serializers.CharField(max_length=100)
    apellido_materno = serializers.CharField(max_length=100)
    nombres = serializers.CharField(max_length=200)
    curp = serializers.CharField(max_length=18)
    puesto = serializers.CharField(max_length=100)
    horas_curso = serializers.IntegerField()
    empresa_id = serializers.IntegerField(required=False)
    
    def validate_plantilla_id(self, value):
        """Validar que la plantilla existe"""
        try:
            PlantillaDC3.objects.get(id=value, activo=True)
        except PlantillaDC3.DoesNotExist:
            raise serializers.ValidationError("Plantilla no válida")
        return value
    
    def validate_curp(self, value):
        """Validar formato de CURP"""
        if len(value) != 18:
            raise serializers.ValidationError("CURP debe tener 18 caracteres")
        return value.upper()

class LoginSerializer(serializers.Serializer):
    """Serializer para login"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class RegistroSerializer(serializers.ModelSerializer):
    """Serializer para registro de usuarios"""
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = Usuario
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'rol'
        ]
    
    def validate(self, data):
        """Validar que las contraseñas coincidan"""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return data
    
    def create(self, validated_data):
        """Crear usuario con contraseña encriptada"""
        validated_data.pop('password_confirm')
        user = Usuario.objects.create_user(**validated_data)
        return user
