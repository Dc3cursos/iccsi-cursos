"""
URLs para la API REST de ICCSI
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from iccsi.cursos.api_views import (
    CursoViewSet, OrganizacionViewSet, InscripcionViewSet,
    CertificadoDC3ViewSet, PlantillaDC3ViewSet
)

# Router para las vistas de la API
router = DefaultRouter()
router.register(r'cursos', CursoViewSet, basename='curso')
router.register(r'organizaciones', OrganizacionViewSet, basename='organizacion')
router.register(r'inscripciones', InscripcionViewSet, basename='inscripcion')
router.register(r'certificados', CertificadoDC3ViewSet, basename='certificado')
router.register(r'plantillas', PlantillaDC3ViewSet, basename='plantilla')

# URLs de la API
urlpatterns = [
    # Autenticación JWT
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # URLs del router
    path('', include(router.urls)),
    
    # Endpoints adicionales
    path('auth/profile/', include('iccsi.usuarios.api_urls')),
]

# URLs de la API disponibles
api_urls = [
    # Autenticación
    'POST /api/auth/login/ - Iniciar sesión',
    'POST /api/auth/refresh/ - Renovar token',
    'GET /api/auth/profile/ - Perfil del usuario',
    
    # Cursos
    'GET /api/cursos/ - Lista de cursos',
    'POST /api/cursos/{id}/inscribirse/ - Inscribirse a curso',
    'GET /api/cursos/mis_cursos/ - Mis cursos',
    
    # Organizaciones
    'GET /api/organizaciones/ - Lista de organizaciones',
    
    # Inscripciones
    'GET /api/inscripciones/ - Mis inscripciones',
    
    # Certificados
    'GET /api/certificados/ - Mis certificados',
    'GET /api/certificados/{id}/descargar/ - Descargar PDF',
    
    # Plantillas
    'GET /api/plantillas/ - Plantillas disponibles',
    'GET /api/plantillas/disponibles/ - Plantillas activas',
]
