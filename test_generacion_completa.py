#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccsi.settings')
django.setup()

from datetime import date
from iccsi.cursos.views import generar_pdf_con_plantilla

def test_generacion_completa():
    """Prueba completa de generación de PDF con la plantilla"""
    
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
        'fecha_inicio': date(2025, 8, 16),
        'fecha_fin': date(2025, 8, 16),
        'instructor_nombre': 'EDUARDO MENDIETA ZUÑIGA',
    }
    
    plantilla_id = 10  # Fraternidad Migratoria
    
    print("🔍 Iniciando prueba de generación de PDF...")
    print(f"📋 Datos de prueba:")
    for key, value in data.items():
        print(f"   {key}: {value}")
    print(f"🎨 Plantilla ID: {plantilla_id}")
    
    try:
        # Generar PDF
        print("\n🔄 Generando PDF...")
        pdf_content = generar_pdf_con_plantilla(data, plantilla_id)
        
        # Guardar PDF de prueba
        output_filename = 'test_generacion_completa.pdf'
        with open(output_filename, 'wb') as f:
            f.write(pdf_content)
        
        print(f"✅ PDF generado exitosamente: {output_filename}")
        print(f"📊 Tamaño del PDF: {len(pdf_content)} bytes")
        
        # Verificar que el PDF no esté vacío
        if len(pdf_content) > 1000:
            print("✅ El PDF tiene contenido válido")
        else:
            print("⚠️ El PDF parece estar vacío o corrupto")
            
        return True
        
    except Exception as e:
        print(f"❌ Error al generar PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_generacion_completa()
    if success:
        print("\n🎉 Prueba completada exitosamente")
    else:
        print("\n�� La prueba falló")
