"""
API REST para el sistema ICCSI
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Curso, Organizacion, Inscripcion, CertificadoDC3, PlantillaDC3
from .serializers import (
    CursoSerializer, OrganizacionSerializer, InscripcionSerializer,
    CertificadoDC3Serializer, PlantillaDC3Serializer
)

class CursoViewSet(viewsets.ModelViewSet):
    """
    API para gestionar cursos
    """
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['organizacion', 'profesor']
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre', 'fecha_creacion', 'duracion_horas']
    ordering = ['-fecha_creacion']
    
    def get_paginated_response(self, data):
        """Personalizar respuesta paginada para mostrar más información"""
        response = super().get_paginated_response(data)
        response.data['total_cursos'] = self.get_queryset().count()
        return response

    @action(detail=True, methods=['post'])
    def inscribirse(self, request, pk=None):
        """Inscribirse a un curso"""
        curso = self.get_object()
        usuario = request.user
        
        if Inscripcion.objects.filter(alumno=usuario, curso=curso).exists():
            return Response(
                {'error': 'Ya estás inscrito a este curso'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        inscripcion = Inscripcion.objects.create(
            alumno=usuario,
            curso=curso
        )
        
        serializer = InscripcionSerializer(inscripcion)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def mis_cursos(self, request):
        """Obtener cursos del usuario actual"""
        inscripciones = Inscripcion.objects.filter(alumno=request.user)
        cursos = [inscripcion.curso for inscripcion in inscripciones]
        serializer = self.get_serializer(cursos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def todos(self, request):
        """Obtener todos los cursos sin paginación"""
        cursos = self.get_queryset()
        serializer = self.get_serializer(cursos, many=True)
        return Response({
            'cursos': serializer.data,
            'total': cursos.count(),
            'mensaje': 'Todos los cursos obtenidos exitosamente'
        })

class OrganizacionViewSet(viewsets.ModelViewSet):
    """
    API para gestionar organizaciones
    """
    queryset = Organizacion.objects.all()
    serializer_class = OrganizacionSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = []
    search_fields = ['nombre']

class InscripcionViewSet(viewsets.ModelViewSet):
    """
    API para gestionar inscripciones
    """
    queryset = Inscripcion.objects.all()
    serializer_class = InscripcionSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['alumno', 'curso', 'fecha_inscripcion']

    def get_queryset(self):
        """Solo mostrar inscripciones del usuario actual"""
        return Inscripcion.objects.filter(alumno=self.request.user)

class CertificadoDC3ViewSet(viewsets.ModelViewSet):
    """
    API para gestionar certificados DC-3
    """
    queryset = CertificadoDC3.objects.all()
    serializer_class = CertificadoDC3Serializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['inscripcion', 'empresa', 'fecha_emision']

    def get_queryset(self):
        """Solo mostrar certificados del usuario actual"""
        return CertificadoDC3.objects.filter(
            inscripcion__alumno=self.request.user
        )

    @action(detail=True, methods=['get'])
    def descargar(self, request, pk=None):
        """Descargar certificado PDF"""
        certificado = self.get_object()
        if certificado.archivo_pdf:
            from django.http import FileResponse
            return FileResponse(
                certificado.archivo_pdf,
                content_type='application/pdf'
            )
        return Response(
            {'error': 'Certificado no disponible'},
            status=status.HTTP_404_NOT_FOUND
        )

class PlantillaDC3ViewSet(viewsets.ModelViewSet):
    """
    API para gestionar plantillas DC-3
    """
    queryset = PlantillaDC3.objects.filter(activo=True)
    serializer_class = PlantillaDC3Serializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['organizacion', 'empresa']

    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        """Obtener plantillas disponibles"""
        plantillas = self.get_queryset()
        serializer = self.get_serializer(plantillas, many=True)
        return Response(serializer.data)
