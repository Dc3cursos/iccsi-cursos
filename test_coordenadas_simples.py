#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccsi.settings')
django.setup()

from datetime import date
from iccsi.cursos.views import generar_pdf_con_plantilla

def test_coordenadas_simples():
    """Prueba el sistema de coordenadas simples"""
    
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
    
    plantilla_id = 10
    
    print("🎯 Generando PDF con coordenadas simples...")
    print(f"📋 Nombre: {data['apellido_paterno']} {data['apellido_materno']} {data['nombres']}")
    print(f"🆔 CURP: {data['curp']}")
    print(f"🏢 RFC: {data['rfc_empresa']}")
    print(f"📅 Fechas: {data['fecha_inicio']} - {data['fecha_fin']}")
    print(f"📚 Curso: {data['nombre_curso']}")
    
    try:
        # Generar PDF con coordenadas simples
        pdf_content = generar_pdf_con_plantilla(data, plantilla_id)
        
        # Guardar el PDF
        filename = f"DC3_coordenadas_simples_{data['apellido_paterno']}_{data['apellido_materno']}_{data['nombres']}_{data['fecha_inicio'].strftime('%Y%m%d')}.pdf"
        
        with open(filename, 'wb') as f:
            f.write(pdf_content)
        
        print(f"✅ PDF generado exitosamente: {filename}")
        print(f"📊 Tamaño del archivo: {len(pdf_content)} bytes")
        print("🎯 Sistema de coordenadas simples activado:")
        print("   - ✅ Coordenadas fáciles de modificar en el código")
        print("   - ✅ CURP y RFC como texto normal")
        print("   - ✅ Fechas en formato YYYYMMDD")
        print("   - ✅ Tú puedes ajustar las coordenadas directamente")
        
    except Exception as e:
        print(f"❌ Error al generar PDF: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_coordenadas_simples()
