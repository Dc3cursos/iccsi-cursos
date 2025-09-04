from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg
from iccsi.cursos.models import Curso, Inscripcion, CertificadoDC3, Organizacion
from datetime import datetime, timedelta
import random

def home(request):
    """Página principal para usuarios no autenticados"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    # Obtener cursos destacados para la página principal
    cursos_destacados = Curso.objects.all()[:6]
    
    # Estadísticas reales desde la base de datos
    total_cursos = Curso.objects.count()
    total_organizaciones = Organizacion.objects.count()
    total_inscripciones = Inscripcion.objects.count()
    total_estudiantes = Inscripcion.objects.values('alumno').distinct().count()
    
    context = {
        'cursos_destacados': cursos_destacados,
        'total_cursos': total_cursos,
        'total_organizaciones': total_organizaciones,
        'total_inscripciones': total_inscripciones,
        'total_estudiantes': total_estudiantes,
    }
    return render(request, 'home.html', context)

@login_required
def dashboard(request):
    """Dashboard personalizado para usuarios autenticados"""
    usuario = request.user
    
    # Obtener inscripciones del usuario
    inscripciones = Inscripcion.objects.filter(alumno=usuario).select_related('curso')
    
    # Cursos en progreso (con inscripción pero sin certificado)
    cursos_en_progreso = []
    for inscripcion in inscripciones:
        if not CertificadoDC3.objects.filter(inscripcion=inscripcion).exists():
            cursos_en_progreso.append(inscripcion.curso)
    
    # Cursos completados (con certificado)
    cursos_completados = []
    for inscripcion in inscripciones:
        if CertificadoDC3.objects.filter(inscripcion=inscripcion).exists():
            cursos_completados.append(inscripcion.curso)
    
    # Cursos recomendados (basados en categorías que el usuario ya ha tomado)
    categorias_interes = set()
    for inscripcion in inscripciones:
        if inscripcion.curso.organizacion:
            categorias_interes.add(inscripcion.curso.organizacion.nombre)
    
    cursos_recomendados = Curso.objects.filter(
        organizacion__nombre__in=categorias_interes
    ).exclude(
        inscripciones__alumno=usuario
    ).distinct()[:6]
    
    # Si no hay suficientes recomendaciones, agregar cursos populares
    if len(cursos_recomendados) < 6:
        cursos_populares = Curso.objects.annotate(
            num_inscripciones=Count('inscripciones')
        ).order_by('-num_inscripciones')[:6]
        cursos_recomendados = list(cursos_recomendados) + list(cursos_populares)
        cursos_recomendados = cursos_recomendados[:6]
    
    # Cursos relacionados (basados en el último curso visto)
    cursos_relacionados = []
    if cursos_en_progreso:
        ultimo_curso = cursos_en_progreso[0]
        cursos_relacionados = Curso.objects.filter(
            organizacion=ultimo_curso.organizacion
        ).exclude(
            inscripciones__alumno=usuario
        ).distinct()[:6]
    
    # Estadísticas del usuario
    total_cursos = inscripciones.count()
    cursos_completados_count = len(cursos_completados)
    certificados_obtenidos = CertificadoDC3.objects.filter(inscripcion__alumno=usuario).count()
    
    # Calcular racha de aprendizaje (simulado)
    racha_semanas = random.randint(1, 8)  # Simulado para demostración
    minutos_curso = random.randint(15, 45)  # Simulado
    visitas = random.randint(1, 3)  # Simulado
    
    context = {
        'usuario': usuario,
        'cursos_en_progreso': cursos_en_progreso,
        'cursos_completados': cursos_completados,
        'cursos_recomendados': cursos_recomendados,
        'cursos_relacionados': cursos_relacionados,
        'total_cursos': total_cursos,
        'cursos_completados_count': cursos_completados_count,
        'certificados_obtenidos': certificados_obtenidos,
        'racha_semanas': racha_semanas,
        'minutos_curso': minutos_curso,
        'visitas': visitas,
        'ultimo_curso_visto': cursos_en_progreso[0] if cursos_en_progreso else None,
    }
    
    return render(request, 'dashboard.html', context)
