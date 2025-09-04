from django.urls import path
from . import views

urlpatterns = [
    path('registro/alumno/', views.registro_alumno, name='registro_alumno'),
    path('registro/profesor/', views.registro_profesor, name='registro_profesor'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('panel/', views.panel_usuario, name='panel_usuario'),
    path('panel/profesor/', views.panel_profesor, name='panel_profesor'),
    path('', views.home, name='home'),
    path('terminos/', views.terminos, name='terminos'),
    path('privacidad/', views.privacidad, name='privacidad'),
    path('cookies/', views.cookies, name='cookies'),
    path('aviso-legal/', views.aviso_legal, name='aviso_legal'),
    path('reportar-falsificacion/', views.reportar_falsificacion, name='reportar_falsificacion'),
]