#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccsi.settings')
django.setup()

from datetime import date
from iccsi.cursos.views import generar_pdf_con_plantilla

def test_diagnostico_completo():
    """Diagnóstico completo del sistema de generación de PDFs"""
    
    # Datos de prueba
    data = {
        'apellido_paterno': 'AGUILA',
        'apellido_materno': 'MENDIETA', 
        'nombres': 'FERNANDO',
        'curp': 'AUMF970410HDFGNR02',
        'puesto': 'TECNICO',
        'nombre_curso': 'BRIGADA CONTRA INCENDIOS',
        'horas_curso': '4',
        'nombre_empresa': 'ADMINITRACION DE CONDOMINIOS MY HOGAR',
        'rfc_empresa': 'ADMINITRACION',
        'representante_legal': 'MARIA DEL CARMEL GARCIA',
        'representante_trabajadores': 'JUAN CARLOS DE ROSA',
        'fecha_inicio': date(2025, 8, 18),
        'fecha_fin': date(2025, 8, 18),
        'instructor_nombre': 'EDUARDO MENDIETA ZUÑIGA',
    }
    
    plantilla_id = 10
    
    print("🔍 DIAGNÓSTICO COMPLETO DEL SISTEMA")
    print("=" * 50)
    
    print(f"📋 Datos de prueba:")
    print(f"   - Nombre: {data['apellido_paterno']} {data['apellido_materno']} {data['nombres']}")
    print(f"   - CURP: {data['curp']}")
    print(f"   - RFC: {data['rfc_empresa']}")
    print(f"   - Curso: {data['nombre_curso']}")
    print(f"   - Fechas: {data['fecha_inicio']} -> {data['fecha_fin']}")
    print(f"   - Plantilla ID: {plantilla_id}")
    
    print(f"\n🎯 Coordenadas por defecto que se están usando:")
    coordenadas_por_defecto = {
        'nombres': (225, 620),
        'curp': (43, 593),
        'puesto': (77, 578),
        'nombre_curso': (112, 460),
        'horas_curso': (54, 416),
        'nombre_empresa': (200, 525),
        'rfc_empresa': (43, 496),
        'representante_legal': (225, 302),
        'representante_trabajadores': (400, 302),
        'fecha_inicio': (257, 416),
        'fecha_fin': (427, 416),
        'instructor_nombre': (50, 302),
    }
    
    for campo, (x, y) in coordenadas_por_defecto.items():
        print(f"   - {campo}: ({x}, {y})")
    
    print(f"\n⚠️  PROBLEMA IDENTIFICADO:")
    print(f"   - El sistema está usando coordenadas por defecto")
    print(f"   - NO está usando las coordenadas personalizadas del mapeo")
    print(f"   - Necesitas usar el formulario de mapeo para aplicar tus coordenadas")
    
    try:
        # Generar PDF con coordenadas por defecto
        print(f"\n✅ Generando PDF con coordenadas por defecto...")
        pdf_content = generar_pdf_con_plantilla(data, plantilla_id)
        
        filename = f"DC3_diagnostico_{data['apellido_paterno']}_{data['apellido_materno']}_{data['nombres']}_{data['fecha_inicio'].strftime('%Y%m%d')}.pdf"
        
        with open(filename, 'wb') as f:
            f.write(pdf_content)
        
        print(f"✅ PDF generado: {filename}")
        print(f"📊 Tamaño del archivo: {len(pdf_content)} bytes")
        
        print(f"\n🎯 SOLUCIÓN:")
        print(f"   1. Ve a: http://127.0.0.1:8000/cursos/dc3/mapear-coordenadas/")
        print(f"   2. Configura las coordenadas exactas que quieres")
        print(f"   3. Genera el PDF con esas coordenadas personalizadas")
        print(f"   4. O usa: http://127.0.0.1:8000/cursos/dc3/mapeo-caracteres-individuales/")
        print(f"      para coordenadas de caracteres individuales")
        
    except Exception as e:
        print(f"❌ Error al generar PDF: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_diagnostico_completo()
