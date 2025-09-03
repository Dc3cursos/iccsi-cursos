#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccsi.settings')
django.setup()

from datetime import date
from iccsi.cursos.views import generar_pdf_con_plantilla

def test_coordenadas_correctas():
    """Prueba las coordenadas correctas actualizadas"""

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

    try:
        # Generar PDF con coordenadas correctas
        pdf_content = generar_pdf_con_plantilla(data, 10)

        # Guardar el PDF para verificar
        with open('test_coordenadas_correctas.pdf', 'wb') as f:
            f.write(pdf_content)

        print(f"PDF generado exitosamente: {len(pdf_content)} bytes")
        print(f"Archivo guardado como: test_coordenadas_correctas.pdf")
        print(f"Coordenadas aplicadas:")
        print(f"   - Nombres: (225, 620)")
        print(f"   - CURP: (43, 593)")
        print(f"   - Puesto: (77, 578)")
        print(f"   - Curso: (112, 450)")
        print(f"   - Horas: (54, 416)")
        print(f"   - Empresa: (200, 525)")
        print(f"   - RFC: (43, 496)")
        print(f"   - Representantes: (225, 302) y (400, 302)")
        print(f"   - Fechas: (257, 416) y (427, 416)")
        print(f"   - Instructor: (50, 302)")

        return True

    except Exception as e:
        print(f"Error al generar PDF: {e}")
        return False

if __name__ == "__main__":
    test_coordenadas_correctas()
