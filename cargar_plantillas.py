#!/usr/bin/env python
"""
Script para cargar automáticamente las plantillas DC-3 desde el directorio media
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccsi.settings')
django.setup()

from django.core.files import File
from django.core.files.base import ContentFile
from iccsi.cursos.models import PlantillaDC3, Organizacion

def cargar_plantillas():
    """Carga las plantillas PDF desde media/plantillas/dc3/"""
    
    # Ruta de las plantillas
    plantillas_dir = Path('media/plantillas/dc3')
    
    if not plantillas_dir.exists():
        print(f"❌ Directorio no encontrado: {plantillas_dir}")
        return
    
    print(f"🔍 Buscando plantillas en: {plantillas_dir}")
    
    # Buscar archivos PDF
    archivos_pdf = list(plantillas_dir.glob('*.pdf'))
    
    if not archivos_pdf:
        print("❌ No se encontraron archivos PDF")
        return
    
    print(f"📄 Encontrados {len(archivos_pdf)} archivos PDF:")
    
    for archivo in archivos_pdf:
        print(f"  - {archivo.name}")
    
    # Cargar cada plantilla
    for archivo in archivos_pdf:
        nombre_plantilla = archivo.stem  # Nombre sin extensión
        
        # Verificar si ya existe
        if PlantillaDC3.objects.filter(nombre=nombre_plantilla).exists():
            print(f"⚠️  La plantilla '{nombre_plantilla}' ya existe, actualizando...")
            plantilla = PlantillaDC3.objects.get(nombre=nombre_plantilla)
        else:
            print(f"➕ Creando nueva plantilla: {nombre_plantilla}")
            plantilla = PlantillaDC3()
            plantilla.nombre = nombre_plantilla
        
        # Actualizar archivo
        with open(archivo, 'rb') as f:
            plantilla.archivo.save(archivo.name, File(f), save=False)
        
        # Configurar según el nombre
        if 'FRATERNIDAD' in nombre_plantilla.upper():
            # Crear o obtener la organización Fraternidad Migratoria
            organizacion, created = Organizacion.objects.get_or_create(
                nombre='Fraternidad Migratoria'
            )
            plantilla.organizacion = organizacion
            plantilla.activo = True
            print(f"  ✅ Configurada para Fraternidad Migratoria")
        elif 'CPI' in nombre_plantilla.upper():
            # Crear o obtener la organización CPI
            organizacion, created = Organizacion.objects.get_or_create(
                nombre='CPI'
            )
            plantilla.organizacion = organizacion
            plantilla.activo = True
            print(f"  ✅ Configurada para CPI")
        else:
            plantilla.activo = True
            print(f"  ✅ Configurada como plantilla general")
        
        plantilla.save()
        print(f"  💾 Guardada: {plantilla.archivo.name}")
    
    print("\n🎉 Carga de plantillas completada!")
    
    # Mostrar resumen
    print("\n📋 Plantillas disponibles:")
    for plantilla in PlantillaDC3.objects.filter(activo=True):
        print(f"  - {plantilla.nombre} ({plantilla.organizacion or 'General'})")

if __name__ == '__main__':
    cargar_plantillas()
