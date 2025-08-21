#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccsi.settings')
django.setup()

from datetime import date
from iccsi.cursos.views import generar_pdf_con_caracteres_individuales

def test_fechas_corregidas():
    """Prueba las fechas con el mapeo corregido"""

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

    # Coordenadas de caracteres individuales
    coordenadas_caracteres = {}
    
    # CURP - 18 caracteres
    curp_coords = [43, 58, 72, 88, 102, 117, 132, 145, 158, 172, 187, 201, 217, 233, 250, 265, 279, 297]
    for i, x in enumerate(curp_coords):
        coordenadas_caracteres[f'curp_{i}'] = (x, 593)
    
    # RFC - 13 caracteres
    rfc_coords = [45, 58, 72, 90, 118, 132, 144, 157, 172, 186, 217, 233, 250]
    for i, x in enumerate(rfc_coords):
        coordenadas_caracteres[f'rfc_{i}'] = (x, 496)
    
    # Fecha Inicio - 10 caracteres (con huecos para las barras)
    fecha_ini_coords = [260, 277, 292, 308, None, 327, 347, None, 368, 390]
    for i, x in enumerate(fecha_ini_coords):
        if x is not None:
            coordenadas_caracteres[f'fecha_ini_{i}'] = (x, 416)
    
    # Fecha Fin - 10 caracteres (con huecos para las barras)
    fecha_fin_coords = [431, 450, 470, 487, None, 510, 530, None, 550, 570]
    for i, x in enumerate(fecha_fin_coords):
        if x is not None:
            coordenadas_caracteres[f'fecha_fin_{i}'] = (x, 416)

    try:
        # Generar PDF con caracteres individuales
        pdf_content = generar_pdf_con_caracteres_individuales(data, 10, coordenadas_caracteres)

        # Guardar el PDF para verificar
        with open('test_fechas_corregidas.pdf', 'wb') as f:
            f.write(pdf_content)

        print(f"PDF generado exitosamente: {len(pdf_content)} bytes")
        print(f"Archivo guardado como: test_fechas_corregidas.pdf")
        print(f"Fecha de prueba: 2025-08-16")
        print(f"Formato esperado: 20250816 (sin barras)")
        print(f"Mapeo de índices:")
        print(f"   UI[0] -> fecha[0] = 2")
        print(f"   UI[1] -> fecha[1] = 0")
        print(f"   UI[2] -> fecha[2] = 2")
        print(f"   UI[3] -> fecha[3] = 5")
        print(f"   UI[4] -> (hueco, era /)")
        print(f"   UI[5] -> fecha[4] = 0")
        print(f"   UI[6] -> fecha[5] = 8")
        print(f"   UI[7] -> (hueco, era /)")
        print(f"   UI[8] -> fecha[6] = 1")
        print(f"   UI[9] -> fecha[7] = 6")
        return True

    except Exception as e:
        print(f"Error al generar PDF: {e}")
        return False

if __name__ == "__main__":
    test_fechas_corregidas()
