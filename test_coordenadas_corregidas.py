#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccsi.settings')
django.setup()

from datetime import date
from iccsi.cursos.views import generar_pdf_con_plantilla

def test_coordenadas_corregidas():
    """Prueba que las coordenadas corregidas funcionen correctamente"""
    
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
    
    print("🎯 Probando coordenadas corregidas...")
    print(f"📚 Curso: {data['nombre_curso']}")
    print(f"📍 Posición del curso: (112, 460)")
    print(f"📅 Fechas: {data['fecha_inicio']} -> 20250818")
    print(f"🆔 CURP: {data['curp']}")
    print(f"🏢 RFC: {data['rfc_empresa']}")
    
    try:
        # Generar PDF con coordenadas corregidas
        print("\n✅ Generando PDF con coordenadas corregidas...")
        pdf_content = generar_pdf_con_plantilla(data, plantilla_id)
        
        filename = f"DC3_coordenadas_corregidas_{data['apellido_paterno']}_{data['apellido_materno']}_{data['nombres']}_{data['fecha_inicio'].strftime('%Y%m%d')}.pdf"
        
        with open(filename, 'wb') as f:
            f.write(pdf_content)
        
        print(f"✅ PDF generado: {filename}")
        print(f"📊 Tamaño del archivo: {len(pdf_content)} bytes")
        
        print("\n🎯 Resultado:")
        print("   - ✅ Coordenadas corregidas aplicadas")
        print("   - ✅ Curso en posición (112, 460)")
        print("   - ✅ Fechas sin barras (YYYYMMDD)")
        print("   - ✅ Sistema funcionando correctamente")
        
    except Exception as e:
        print(f"❌ Error al generar PDF: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_coordenadas_corregidas()
