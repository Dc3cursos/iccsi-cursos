from django.shortcuts import render
from django.http import JsonResponse

def home(request):
    """Vista principal de la página de inicio"""
    context = {
        'title': 'ICCSI - Cursos Avanzados',
        'subtitle': 'Plataforma de Cursos Profesionales',
        'description': 'Accede a cursos de alta calidad con certificaciones DC-3',
        'features': [
            'Cursos certificados',
            'Instructores expertos',
            'Material actualizado',
            'Soporte 24/7'
        ]
    }
    return render(request, 'home.html', context)

def api_info(request):
    """Información de la API"""
    return JsonResponse({
        'message': 'ICCSI API funcionando correctamente',
        'version': '1.0.0',
        'status': 'active'
    })
