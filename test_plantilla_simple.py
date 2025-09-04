#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccsi.settings')
django.setup()

from iccsi.cursos.models import PlantillaDC3

def test_plantilla():
    """Prueba simple para verificar que la plantilla existe y se puede cargar"""
    try:
        # Verificar si existe la plantilla con ID 10
        plantilla = PlantillaDC3.objects.get(id=10, activo=True)
        print(f"✅ Plantilla encontrada: {plantilla.nombre}")
        print(f"📁 Archivo: {plantilla.archivo.path}")
        print(f"📄 Existe archivo: {os.path.exists(plantilla.archivo.path)}")
        
        if os.path.exists(plantilla.archivo.path):
            file_size = os.path.getsize(plantilla.archivo.path)
            print(f"📊 Tamaño del archivo: {file_size} bytes")
            
            # Intentar leer el archivo
            with open(plantilla.archivo.path, 'rb') as f:
                content = f.read()
                print(f"✅ Archivo leído correctamente: {len(content)} bytes")
                
        else:
            print("❌ El archivo de la plantilla no existe")
            
    except PlantillaDC3.DoesNotExist:
        print("❌ No se encontró la plantilla con ID 10")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_plantilla()
