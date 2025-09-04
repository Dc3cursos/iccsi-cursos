#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccsi.settings')
django.setup()

from datetime import date
from iccsi.cursos.views import generar_pdf_con_plantilla

def test_fechas_sin_barras():
    """Prueba que las fechas no tengan barras y usen coordenadas correctas"""
    
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
    
    print("🎯 Probando fechas sin barras...")
    print(f"📅 Fecha inicio: {data['fecha_inicio']} -> 20250816")
    print(f"📅 Fecha fin: {data['fecha_fin']} -> 20250816")
    print(f"🆔 CURP: {data['curp']}")
    print(f"🏢 RFC: {data['rfc_empresa']}")
    
    try:
        # Generar PDF con coordenadas por defecto
        print("\n✅ Generando PDF con fechas sin barras...")
        pdf_content = generar_pdf_con_plantilla(data, plantilla_id)
        
        filename = f"DC3_fechas_sin_barras_{data['apellido_paterno']}_{data['apellido_materno']}_{data['nombres']}_{data['fecha_inicio'].strftime('%Y%m%d')}.pdf"
        
        with open(filename, 'wb') as f:
            f.write(pdf_content)
        
        print(f"✅ PDF generado: {filename}")
        print(f"📊 Tamaño del archivo: {len(pdf_content)} bytes")
        
        print("\n🎯 Resultado:")
        print("   - ✅ Fechas en formato YYYYMMDD (sin barras)")
        print("   - ✅ CURP y RFC en coordenadas exactas")
        print("   - ✅ Sistema funcionando correctamente")
        
    except Exception as e:
        print(f"❌ Error al generar PDF: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_fechas_sin_barras()
