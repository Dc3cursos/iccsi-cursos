#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccsi.settings')
django.setup()

from iccsi.cursos.views import generar_pdf_con_caracteres_individuales
from datetime import date

def test_nombre_formato():
    """Prueba el formato del nombre: APELLIDOS + NOMBRES"""
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
    
    # Coordenadas de caracteres individuales (las que ya tienes funcionando)
    coordenadas_caracteres = {}
    
    # CURP - 18 caracteres
    for i in range(18):
        coordenadas_caracteres[f'curp_{i}'] = (43 + (i * 6), 593)
    
    # RFC - 13 caracteres
    for i in range(13):
        coordenadas_caracteres[f'rfc_{i}'] = (43 + (i * 6), 496)
    
    # Fecha Inicio - 10 caracteres
    for i in range(10):
        coordenadas_caracteres[f'fecha_ini_{i}'] = (257 + (i * 6), 416)
    
    # Fecha Fin - 10 caracteres
    for i in range(10):
        coordenadas_caracteres[f'fecha_fin_{i}'] = (427 + (i * 6), 416)
    
    plantilla_id = 10  # Fraternidad Migratoria
    
    try:
        pdf_content = generar_pdf_con_caracteres_individuales(data, plantilla_id, coordenadas_caracteres)
        
        with open('test_nombre_formato.pdf', 'wb') as f:
            f.write(pdf_content)
        
        # Verificar el formato del nombre
        apellido_paterno = data['apellido_paterno']
        apellido_materno = data['apellido_materno']
        nombres = data['nombres']
        nombre_completo = f"{apellido_paterno} {apellido_materno} {nombres}".strip()
        
        print("✅ PDF de prueba generado: test_nombre_formato.pdf")
        print(f"📝 Formato del nombre: {nombre_completo}")
        print(f"   - Apellido Paterno: {apellido_paterno}")
        print(f"   - Apellido Materno: {apellido_materno}")
        print(f"   - Nombres: {nombres}")
        print("🔤 CURP y RFC: caracteres individuales")
        print("📅 Fechas: formato YYYY/MM/DD")
        print("📊 Tamaño del PDF:", len(pdf_content), "bytes")
        
    except Exception as e:
        print(f"❌ Error al generar PDF: {e}")

if __name__ == '__main__':
    test_nombre_formato()
