#!/usr/bin/env python
"""
Script para ajustar coordenadas de la plantilla PDF
Genera PDFs de prueba con diferentes posiciones para encontrar las coordenadas correctas
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccsi.settings')
django.setup()

from iccsi.cursos.views import generar_pdf_con_plantilla
from datetime import date

def generar_pdf_con_coordenadas_test():
    """Genera un PDF de prueba con coordenadas ajustables"""
    
    # Datos de prueba
    data = {
        'apellido_paterno': 'AGUILA',
        'apellido_materno': 'MENDIETA', 
        'nombres': 'FERNANDO',
        'curp': 'AUMF970410HDFGNR02',
        'puesto': 'TECNICO',
        'ocupacion': 'TECNICO EN SEGURIDAD',
        'nombre_curso': 'BRIGADA CONTRA INCENDIOS',
        'horas_curso': '4',
        'area_tematica': '6000',
        'nombre_empresa': 'ADMINITRACION DE CONDOMINIOS MY HOGAR',
        'rfc_empresa': 'ADMINITRACION',
        'representante_legal': 'MARIA DEL CARMEL GARCIA',
        'representante_trabajadores': 'JUAN CARLOS DE ROSA',
        'fecha_inicio': date(2025, 8, 15),
        'fecha_fin': date(2025, 8, 15),
        'instructor_nombre': 'EDUARDO MENDIETA ZUÑIGA',
    }
    
    # Diferentes configuraciones de coordenadas para probar
    configuraciones = {
        'config1': {
            'nombres': (250, 700),
            'curp': (250, 670),
            'puesto': (250, 640),
            'ocupacion': (250, 610),
            'nombre_curso': (250, 580),
            'horas_curso': (250, 550),
            'area_tematica': (250, 520),
            'nombre_empresa': (250, 490),
            'rfc_empresa': (250, 460),
            'representante_legal': (250, 430),
            'representante_trabajadores': (250, 400),
            'fecha_inicio': (250, 370),
            'fecha_fin': (250, 340),
            'instructor_nombre': (250, 310),
        },
        'config2': {
            'nombres': (350, 700),
            'curp': (350, 670),
            'puesto': (350, 640),
            'ocupacion': (350, 610),
            'nombre_curso': (350, 580),
            'horas_curso': (350, 550),
            'area_tematica': (350, 520),
            'nombre_empresa': (350, 490),
            'rfc_empresa': (350, 460),
            'representante_legal': (350, 430),
            'representante_trabajadores': (350, 400),
            'fecha_inicio': (350, 370),
            'fecha_fin': (350, 340),
            'instructor_nombre': (350, 310),
        },
        'config3': {
            'nombres': (400, 650),
            'curp': (400, 620),
            'puesto': (400, 590),
            'ocupacion': (400, 560),
            'nombre_curso': (400, 530),
            'horas_curso': (400, 500),
            'area_tematica': (400, 470),
            'nombre_empresa': (400, 440),
            'rfc_empresa': (400, 410),
            'representante_legal': (400, 380),
            'representante_trabajadores': (400, 350),
            'fecha_inicio': (400, 320),
            'fecha_fin': (400, 290),
            'instructor_nombre': (400, 260),
        }
    }
    
    for config_name, posiciones in configuraciones.items():
        try:
            print(f"🧪 Generando PDF con {config_name}...")
            
            # Modificar temporalmente las coordenadas en la función
            from iccsi.cursos.views import generar_pdf_con_plantilla
            
            # Crear una versión modificada de la función con las coordenadas de prueba
            def generar_pdf_con_coordenadas_test(data, plantilla_id, posiciones_test):
                from PyPDF2 import PdfReader, PdfWriter
                from reportlab.pdfgen import canvas
                from reportlab.lib.pagesizes import letter
                from reportlab.lib.colors import black
                import io
                from datetime import datetime
                from iccsi.cursos.models import PlantillaDC3
                
                # Obtener la plantilla
                plantilla = PlantillaDC3.objects.get(id=plantilla_id, activo=True)
                
                # Leer la plantilla PDF
                with open(plantilla.archivo.path, 'rb') as template_file:
                    template_reader = PdfReader(template_file)
                    template_page = template_reader.pages[0]
                    
                    # Crear un nuevo PDF con los datos
                    output = PdfWriter()
                    
                    # Crear un PDF temporal con los datos del formulario
                    data_pdf = io.BytesIO()
                    c = canvas.Canvas(data_pdf)
                    
                    # Configurar fuente y tamaño
                    c.setFont("Helvetica", 10)
                    
                    # Escribir los datos en el PDF usando las coordenadas de prueba
                    for campo, (x, y) in posiciones_test.items():
                        if campo in ['nombres', 'apellido_paterno', 'apellido_materno']:
                            # Combinar nombre completo en una sola línea
                            nombre_completo = f"{data.get('nombres', '')} {data.get('apellido_paterno', '')} {data.get('apellido_materno', '')}".strip()
                            if campo == 'nombres':  # Solo escribir una vez
                                c.drawString(x, y, nombre_completo)
                            continue
                        elif campo in ['apellido_paterno', 'apellido_materno']:
                            continue  # Ya se manejó arriba
                        else:
                            valor = data.get(campo, '')
                            if hasattr(valor, 'strftime'):  # Verificar si es una fecha
                                valor = valor.strftime('%d/%m/%Y')
                            c.drawString(x, y, str(valor))
                    
                    c.save()
                    data_pdf.seek(0)
                    
                    # Combinar la plantilla con los datos
                    data_reader = PdfReader(data_pdf)
                    data_page = data_reader.pages[0]
                    
                    # Superponer los datos sobre la plantilla
                    template_page.merge_page(data_page)
                    output.add_page(template_page)
                    
                    # Generar el PDF final
                    result_pdf = io.BytesIO()
                    output.write(result_pdf)
                    result_pdf.seek(0)
                    
                    return result_pdf.getvalue()
            
            # Generar PDF con coordenadas de prueba
            pdf_content = generar_pdf_con_coordenadas_test(data, 10, posiciones)
            
            # Guardar el PDF de prueba
            filename = f'test_coordenadas_{config_name}.pdf'
            with open(filename, 'wb') as f:
                f.write(pdf_content)
            print(f"✅ PDF guardado como '{filename}' ({len(pdf_content)} bytes)")
            
        except Exception as e:
            print(f"❌ Error al generar PDF con {config_name}: {e}")

if __name__ == "__main__":
    generar_pdf_con_coordenadas_test()
