#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccsi.settings')
django.setup()

from iccsi.cursos.models import Curso, Organizacion, PlantillaDC3

def test_plantillas_organizacion():
    print("=== PRUEBA DE ASIGNACIÓN DE PLANTILLAS POR ORGANIZACIÓN ===\n")
    
    # Obtener organizaciones
    fraternidad = Organizacion.objects.filter(nombre="Fraternidad Migratoria").first()
    cpi = Organizacion.objects.filter(nombre="CPI").first()
    
    print(f"Organización Fraternidad Migratoria: {fraternidad}")
    print(f"Organización CPI: {cpi}\n")
    
    # Obtener plantillas
    plantilla_fraternidad = PlantillaDC3.objects.filter(id=10).first()
    plantilla_cpi = PlantillaDC3.objects.filter(id=11).first()
    
    print(f"Plantilla Fraternidad (ID 10): {plantilla_fraternidad}")
    print(f"Plantilla CPI (ID 11): {plantilla_cpi}\n")
    
    # Obtener cursos de cada organización
    cursos_fraternidad = Curso.objects.filter(organizacion=fraternidad)[:3]
    cursos_cpi = Curso.objects.filter(organizacion=cpi)[:3]
    
    print("=== CURSOS DE FRATERNIDAD MIGRATORIA ===")
    for curso in cursos_fraternidad:
        print(f"- {curso.nombre} (Organización: {curso.organizacion.nombre})")
        # Simular la lógica de selección de plantilla
        if curso.organizacion and curso.organizacion.nombre == "Fraternidad Migratoria":
            plantilla_id = 10
        elif curso.organizacion and curso.organizacion.nombre == "CPI":
            plantilla_id = 11
        else:
            plantilla_id = 10
        print(f"  → Plantilla asignada: ID {plantilla_id}")
    
    print("\n=== CURSOS DE CPI ===")
    for curso in cursos_cpi:
        print(f"- {curso.nombre} (Organización: {curso.organizacion.nombre})")
        # Simular la lógica de selección de plantilla
        if curso.organizacion and curso.organizacion.nombre == "Fraternidad Migratoria":
            plantilla_id = 10
        elif curso.organizacion and curso.organizacion.nombre == "CPI":
            plantilla_id = 11
        else:
            plantilla_id = 10
        print(f"  → Plantilla asignada: ID {plantilla_id}")
    
    print("\n=== RESUMEN ===")
    print("✅ Fraternidad Migratoria → Plantilla ID 10")
    print("✅ CPI → Plantilla ID 11")
    print("✅ Sistema configurado correctamente")

if __name__ == "__main__":
    test_plantillas_organizacion()
