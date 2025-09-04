"""
Vistas de API para usuarios
"""
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UsuarioSerializer
from .models import Usuario

class UserProfileView(generics.RetrieveAPIView):
    """
    Vista para obtener el perfil del usuario actual
    """
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get_object(self):
        """Retornar el usuario actual"""
        return self.request.user
