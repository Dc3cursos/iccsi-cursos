#!/usr/bin/env python
"""
Script de prueba para verificar el procesamiento de plantillas PDF
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccsi.settings')
django.setup()

from iccsi.cursos.views import generar_pdf_con_plantilla
from datetime import date

def test_plantilla():
    """Prueba la generación de PDF con plantilla"""
    
    # Datos de prueba
    data = {
        'apellido_paterno': 'AGUILA',
        'apellido_materno': 'MENDIETA', 
        'nombres': 'FERNANDO',
        'curp': 'AUMF970410HDFGNR02',
        'puesto': 'TECNICO',
        'ocupacion': 'TECNICO EN SEGURIDAD',
        'nombre_curso': 'BRIGADA CONTRA INCENDIOS',
        'horas_curso': '4',
        'area_tematica': '6000',
        'nombre_empresa': 'ADMINITRACION DE CONDOMINIOS MY HOGAR',
        'rfc_empresa': 'ADMINITRACION',
        'representante_legal': 'MARIA DEL CARMEL GARCIA',
        'representante_trabajadores': 'JUAN CARLOS DE ROSA',
        'fecha_inicio': date(2025, 8, 15),
        'fecha_fin': date(2025, 8, 15),
        'instructor_nombre': 'EDUARDO MENDIETA ZUÑIGA',
    }
    
    try:
        print("🧪 Probando generación de PDF con plantilla...")
        pdf_content = generar_pdf_con_plantilla(data, 10)
        print(f"✅ PDF generado exitosamente: {len(pdf_content)} bytes")
        
        # Guardar el PDF de prueba
        with open('test_plantilla.pdf', 'wb') as f:
            f.write(pdf_content)
        print("💾 PDF guardado como 'test_plantilla.pdf'")
        
    except Exception as e:
        print(f"❌ Error al generar PDF: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_plantilla()
