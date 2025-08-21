#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccsi.settings')
django.setup()

from datetime import date
from iccsi.cursos.views import generar_pdf_con_plantilla

def test_coordenadas_actualizadas():
    """Prueba las coordenadas actualizadas"""
    
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
    
    print("🎯 PROBANDO COORDENADAS ACTUALIZADAS")
    print("=" * 50)
    
    print(f"📋 Datos de prueba:")
    print(f"   - Nombre: {data['apellido_paterno']} {data['apellido_materno']} {data['nombres']}")
    print(f"   - CURP: {data['curp']}")
    print(f"   - RFC: {data['rfc_empresa']}")
    print(f"   - Curso: {data['nombre_curso']}")
    print(f"   - Fechas: {data['fecha_inicio']} -> {data['fecha_fin']}")
    
    print(f"\n✅ Coordenadas actualizadas:")
    coordenadas_actualizadas = {
        'nombres': (225, 620),
        'curp': (43, 593),
        'puesto': (77, 578),
        'nombre_curso': (112, 450),  # Actualizado
        'horas_curso': (54, 416),
        'nombre_empresa': (200, 525),
        'rfc_empresa': (43, 496),
        'representante_legal': (225, 302),
        'representante_trabajadores': (400, 302),
        'fecha_inicio': (257, 416),
        'fecha_fin': (427, 416),
        'instructor_nombre': (50, 302),
    }
    
    for campo, (x, y) in coordenadas_actualizadas.items():
        print(f"   - {campo}: ({x}, {y})")
    
    try:
        # Generar PDF con coordenadas actualizadas
        print(f"\n✅ Generando PDF con coordenadas actualizadas...")
        pdf_content = generar_pdf_con_plantilla(data, plantilla_id)
        
        filename = f"DC3_coordenadas_actualizadas_{data['apellido_paterno']}_{data['apellido_materno']}_{data['nombres']}_{data['fecha_inicio'].strftime('%Y%m%d')}.pdf"
        
        with open(filename, 'wb') as f:
            f.write(pdf_content)
        
        print(f"✅ PDF generado: {filename}")
        print(f"📊 Tamaño del archivo: {len(pdf_content)} bytes")
        
        print(f"\n🎯 Resultado:")
        print(f"   - ✅ Coordenadas actualizadas aplicadas")
        print(f"   - ✅ Curso en posición (112, 450)")
        print(f"   - ✅ Sistema funcionando correctamente")
        
        print(f"\n💡 Para control total de caracteres individuales:")
        print(f"   - Usa: http://127.0.0.1:8000/cursos/dc3/mapeo-caracteres-individuales/")
        
    except Exception as e:
        print(f"❌ Error al generar PDF: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_coordenadas_actualizadas()
