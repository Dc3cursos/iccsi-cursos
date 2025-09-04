"""
URLs de la API para usuarios
"""
from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.UserProfileView.as_view(), name='user_profile'),
]
