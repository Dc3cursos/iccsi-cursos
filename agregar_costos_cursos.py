#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccsi.iccsi.settings')
django.setup()

from iccsi.cursos.models import Curso, CostoCurso

def agregar_costos_cursos():
    """Agregar costos de 380 pesos a todos los cursos que no tengan costo"""
    print("🔍 Buscando cursos sin costo...")
    
    cursos_sin_costo = []
    for curso in Curso.objects.all():
        try:
            costo = curso.costo
            print(f"✅ Curso '{curso.nombre}' ya tiene costo: ${costo.precio} {costo.moneda}")
        except CostoCurso.DoesNotExist:
            cursos_sin_costo.append(curso)
    
    if not cursos_sin_costo:
        print("🎉 Todos los cursos ya tienen costo configurado.")
        return
    
    print(f"\n📝 Encontrados {len(cursos_sin_costo)} cursos sin costo.")
    print("💰 Agregando costo de $380.00 MXN a cada curso...")
    
    for curso in cursos_sin_costo:
        costo = CostoCurso.objects.create(
            curso=curso,
            precio=380.00,
            moneda='MXN',
            activo=True
        )
        print(f"✅ Agregado costo ${costo.precio} {costo.moneda} al curso: {curso.nombre}")
    
    print(f"\n🎉 Proceso completado. Se agregaron costos a {len(cursos_sin_costo)} cursos.")

if __name__ == '__main__':
    agregar_costos_cursos()
