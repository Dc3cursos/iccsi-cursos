from django.urls import path
from . import views

urlpatterns = [
    path('registro/alumno/', views.registro_alumno, name='registro_alumno'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('panel/', views.panel_usuario, name='panel_usuario'),
    path('', views.home, name='home'),
]