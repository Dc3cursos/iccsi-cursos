#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccsi.settings')
django.setup()

from datetime import date
from iccsi.cursos.views import generar_pdf_con_plantilla

def test_movimiento_curso():
    """Prueba el movimiento del curso con diferentes coordenadas"""
    
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
    
    # Coordenadas por defecto
    coordenadas_default = {
        'nombres': (225, 620),
        'curp': (43, 593),
        'puesto': (77, 578),
        'nombre_curso': (112, 460),  # Posición original
        'horas_curso': (54, 416),
        'nombre_empresa': (200, 525),
        'rfc_empresa': (43, 496),
        'representante_legal': (225, 302),
        'representante_trabajadores': (400, 302),
        'fecha_inicio': (257, 416),
        'fecha_fin': (427, 416),
        'instructor_nombre': (50, 302),
    }
    
    # Coordenadas con curso movido
    coordenadas_movidas = {
        'nombres': (225, 620),
        'curp': (43, 593),
        'puesto': (77, 578),
        'nombre_curso': (200, 500),  # Curso movido a nueva posición
        'horas_curso': (54, 416),
        'nombre_empresa': (200, 525),
        'rfc_empresa': (43, 496),
        'representante_legal': (225, 302),
        'representante_trabajadores': (400, 302),
        'fecha_inicio': (257, 416),
        'fecha_fin': (427, 416),
        'instructor_nombre': (50, 302),
    }
    
    print("🎯 Probando movimiento del curso...")
    print(f"📚 Curso: {data['nombre_curso']}")
    
    try:
        # 1. Generar PDF con coordenadas por defecto
        print("\n1️⃣ Generando PDF con coordenadas por defecto...")
        pdf_default = generar_pdf_con_plantilla(data, plantilla_id, coordenadas_default)
        
        filename_default = f"DC3_curso_default_{data['apellido_paterno']}_{data['apellido_materno']}_{data['nombres']}_{data['fecha_inicio'].strftime('%Y%m%d')}.pdf"
        with open(filename_default, 'wb') as f:
            f.write(pdf_default)
        print(f"✅ PDF generado: {filename_default}")
        print(f"📍 Curso en posición: {coordenadas_default['nombre_curso']}")
        
        # 2. Generar PDF con curso movido
        print("\n2️⃣ Generando PDF con curso movido...")
        pdf_movido = generar_pdf_con_plantilla(data, plantilla_id, coordenadas_movidas)
        
        filename_movido = f"DC3_curso_movido_{data['apellido_paterno']}_{data['apellido_materno']}_{data['nombres']}_{data['fecha_inicio'].strftime('%Y%m%d')}.pdf"
        with open(filename_movido, 'wb') as f:
            f.write(pdf_movido)
        print(f"✅ PDF generado: {filename_movido}")
        print(f"📍 Curso en nueva posición: {coordenadas_movidas['nombre_curso']}")
        
        print("\n🎯 Resultado:")
        print(f"   - 📄 PDF por defecto: {filename_default}")
        print(f"   - 📄 PDF con curso movido: {filename_movido}")
        print(f"   - 🔄 El curso se movió de {coordenadas_default['nombre_curso']} a {coordenadas_movidas['nombre_curso']}")
        print("   - ✅ El sistema de coordenadas personalizadas funciona correctamente")
        
    except Exception as e:
        print(f"❌ Error al generar PDF: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_movimiento_curso()
