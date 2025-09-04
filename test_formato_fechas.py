#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccsi.settings')
django.setup()

from iccsi.cursos.views import generar_pdf_con_plantilla
from datetime import date

def test_formato_fechas():
    """Prueba el nuevo formato de fechas YYYY/MM/DD"""
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
    
    try:
        pdf_content = generar_pdf_con_plantilla(data, plantilla_id)
        
        with open('test_formato_fechas.pdf', 'wb') as f:
            f.write(pdf_content)
        
        print("✅ PDF de prueba generado: test_formato_fechas.pdf")
        print("📅 Formato de fechas: YYYY/MM/DD")
        print("🔤 CURP y RFC: caracteres individuales con espaciado 6")
        print("📊 Tamaño del PDF:", len(pdf_content), "bytes")
        
    except Exception as e:
        print(f"❌ Error al generar PDF: {e}")

if __name__ == '__main__':
    test_formato_fechas()
