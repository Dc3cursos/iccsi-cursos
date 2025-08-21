#!/usr/bin/env python
"""
Script para ajustar coordenadas con mayor precisión
Permite ajustar cada campo individualmente con coordenadas más específicas
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccsi.settings')
django.setup()

from datetime import date

def generar_pdf_con_coordenadas_precisas():
    """Genera PDFs con coordenadas más precisas y ajustables"""
    
    from PyPDF2 import PdfReader, PdfWriter
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.colors import black, red, blue, green
    import io
    from iccsi.cursos.models import PlantillaDC3
    
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
    
    # Obtener la plantilla
    plantilla = PlantillaDC3.objects.get(id=10, activo=True)
    
    # Leer la plantilla PDF
    with open(plantilla.archivo.path, 'rb') as template_file:
        template_reader = PdfReader(template_file)
        template_page = template_reader.pages[0]
        
        # Configuraciones más precisas con diferentes rangos de coordenadas
        configuraciones = {
            'config_1': {
                'nombres': (100, 750),
                'curp': (100, 720),
                'puesto': (100, 690),
                'ocupacion': (100, 660),
                'nombre_curso': (100, 630),
                'horas_curso': (100, 600),
                'area_tematica': (100, 570),
                'nombre_empresa': (100, 540),
                'rfc_empresa': (100, 510),
                'representante_legal': (100, 480),
                'representante_trabajadores': (100, 450),
                'fecha_inicio': (100, 420),
                'fecha_fin': (100, 390),
                'instructor_nombre': (100, 360),
            },
            'config_2': {
                'nombres': (120, 750),
                'curp': (120, 720),
                'puesto': (120, 690),
                'ocupacion': (120, 660),
                'nombre_curso': (120, 630),
                'horas_curso': (120, 600),
                'area_tematica': (120, 570),
                'nombre_empresa': (120, 540),
                'rfc_empresa': (120, 510),
                'representante_legal': (120, 480),
                'representante_trabajadores': (120, 450),
                'fecha_inicio': (120, 420),
                'fecha_fin': (120, 390),
                'instructor_nombre': (120, 360),
            },
            'config_3': {
                'nombres': (140, 750),
                'curp': (140, 720),
                'puesto': (140, 690),
                'ocupacion': (140, 660),
                'nombre_curso': (140, 630),
                'horas_curso': (140, 600),
                'area_tematica': (140, 570),
                'nombre_empresa': (140, 540),
                'rfc_empresa': (140, 510),
                'representante_legal': (140, 480),
                'representante_trabajadores': (140, 450),
                'fecha_inicio': (140, 420),
                'fecha_fin': (140, 390),
                'instructor_nombre': (140, 360),
            },
            'config_4': {
                'nombres': (160, 750),
                'curp': (160, 720),
                'puesto': (160, 690),
                'ocupacion': (160, 660),
                'nombre_curso': (160, 630),
                'horas_curso': (160, 600),
                'area_tematica': (160, 570),
                'nombre_empresa': (160, 540),
                'rfc_empresa': (160, 510),
                'representante_legal': (160, 480),
                'representante_trabajadores': (160, 450),
                'fecha_inicio': (160, 420),
                'fecha_fin': (160, 390),
                'instructor_nombre': (160, 360),
            },
            'config_5': {
                'nombres': (180, 750),
                'curp': (180, 720),
                'puesto': (180, 690),
                'ocupacion': (180, 660),
                'nombre_curso': (180, 630),
                'horas_curso': (180, 600),
                'area_tematica': (180, 570),
                'nombre_empresa': (180, 540),
                'rfc_empresa': (180, 510),
                'representante_legal': (180, 480),
                'representante_trabajadores': (180, 450),
                'fecha_inicio': (180, 420),
                'fecha_fin': (180, 390),
                'instructor_nombre': (180, 360),
            }
        }
        
        # Generar PDF para cada configuración
        for config_name, posiciones in configuraciones.items():
            print(f"🧪 Generando PDF con {config_name}...")
            
            # Crear un nuevo PDF con los datos
            output = PdfWriter()
            
            # Crear un PDF temporal con los datos
            data_pdf = io.BytesIO()
            c = canvas.Canvas(data_pdf)
            
            # Configurar fuente
            c.setFont("Helvetica", 10)
            c.setFillColor(black)
            
            # Escribir los datos en el PDF
            for campo, (x, y) in posiciones.items():
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
            
            # Combinar con la plantilla
            data_reader = PdfReader(data_pdf)
            data_page = data_reader.pages[0]
            
            # Crear una copia de la plantilla para esta configuración
            template_copy = template_page
            template_copy.merge_page(data_page)
            
            # Agregar a un nuevo writer
            output_config = PdfWriter()
            output_config.add_page(template_copy)
            
            # Generar el PDF final
            result_pdf = io.BytesIO()
            output_config.write(result_pdf)
            result_pdf.seek(0)
            
            # Guardar el PDF
            filename = f'ajuste_preciso_{config_name}.pdf'
            with open(filename, 'wb') as f:
                f.write(result_pdf.getvalue())
            print(f"✅ PDF guardado como '{filename}' ({len(result_pdf.getvalue())} bytes)")

def generar_pdf_con_marcadores_especificos():
    """Genera un PDF con marcadores específicos para cada campo"""
    
    from PyPDF2 import PdfReader, PdfWriter
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.colors import black, red, blue, green
    import io
    from iccsi.cursos.models import PlantillaDC3
    
    # Obtener la plantilla
    plantilla = PlantillaDC3.objects.get(id=10, activo=True)
    
    # Leer la plantilla PDF
    with open(plantilla.archivo.path, 'rb') as template_file:
        template_reader = PdfReader(template_file)
        template_page = template_reader.pages[0]
        
        # Crear un nuevo PDF con los datos
        output = PdfWriter()
        
        # Crear un PDF temporal con marcadores específicos
        data_pdf = io.BytesIO()
        c = canvas.Canvas(data_pdf)
        
        # Configurar fuentes
        c.setFont("Helvetica-Bold", 12)
        
        # Marcadores específicos para cada campo con coordenadas más precisas
        marcadores_especificos = [
            # Nombre completo - diferentes posiciones
            (80, 750, "NOMBRE", red),
            (100, 750, "NOMBRE", red),
            (120, 750, "NOMBRE", red),
            (140, 750, "NOMBRE", red),
            (160, 750, "NOMBRE", red),
            (180, 750, "NOMBRE", red),
            (200, 750, "NOMBRE", red),
            
            # CURP - diferentes posiciones
            (80, 720, "CURP", blue),
            (100, 720, "CURP", blue),
            (120, 720, "CURP", blue),
            (140, 720, "CURP", blue),
            (160, 720, "CURP", blue),
            (180, 720, "CURP", blue),
            (200, 720, "CURP", blue),
            
            # Puesto - diferentes posiciones
            (80, 690, "PUESTO", green),
            (100, 690, "PUESTO", green),
            (120, 690, "PUESTO", green),
            (140, 690, "PUESTO", green),
            (160, 690, "PUESTO", green),
            (180, 690, "PUESTO", green),
            (200, 690, "PUESTO", green),
            
            # Curso - diferentes posiciones
            (80, 660, "CURSO", red),
            (100, 660, "CURSO", red),
            (120, 660, "CURSO", red),
            (140, 660, "CURSO", red),
            (160, 660, "CURSO", red),
            (180, 660, "CURSO", red),
            (200, 660, "CURSO", red),
            
            # Empresa - diferentes posiciones
            (80, 630, "EMPRESA", blue),
            (100, 630, "EMPRESA", blue),
            (120, 630, "EMPRESA", blue),
            (140, 630, "EMPRESA", blue),
            (160, 630, "EMPRESA", blue),
            (180, 630, "EMPRESA", blue),
            (200, 630, "EMPRESA", blue),
            
            # Instructor - diferentes posiciones
            (80, 600, "INSTRUCTOR", green),
            (100, 600, "INSTRUCTOR", green),
            (120, 600, "INSTRUCTOR", green),
            (140, 600, "INSTRUCTOR", green),
            (160, 600, "INSTRUCTOR", green),
            (180, 600, "INSTRUCTOR", green),
            (200, 600, "INSTRUCTOR", green),
        ]
        
        # Dibujar marcadores específicos
        for x, y, texto, color in marcadores_especificos:
            # Dibujar un círculo del color correspondiente
            c.setFillColor(color)
            c.circle(x, y, 2, fill=1)
            
            # Dibujar el texto
            c.setFillColor(black)
            c.setFont("Helvetica", 8)
            c.drawString(x + 5, y - 2, texto)
            
            # Dibujar coordenadas
            c.setFont("Helvetica", 6)
            c.drawString(x + 5, y - 12, f"({x},{y})")
        
        # Agregar instrucciones detalladas
        c.setFillColor(black)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, 780, "MARCADORES ESPECÍFICOS POR CAMPO:")
        c.setFont("Helvetica", 10)
        c.drawString(50, 760, "🔴 ROJO = Nombre, Curso")
        c.drawString(50, 745, "🔵 AZUL = CURP, Empresa")
        c.drawString(50, 730, "🟢 VERDE = Puesto, Instructor")
        c.drawString(50, 715, "Los números son las coordenadas (X, Y)")
        
        c.save()
        data_pdf.seek(0)
        
        # Combinar la plantilla con los marcadores
        data_reader = PdfReader(data_pdf)
        data_page = data_reader.pages[0]
        
        # Superponer los marcadores sobre la plantilla
        template_page.merge_page(data_page)
        output.add_page(template_page)
        
        # Generar el PDF final
        result_pdf = io.BytesIO()
        output.write(result_pdf)
        result_pdf.seek(0)
        
        return result_pdf.getvalue()

if __name__ == "__main__":
    print("🔍 Generando PDF con marcadores específicos por campo...")
    try:
        pdf_content = generar_pdf_con_marcadores_especificos()
        filename = 'marcadores_especificos.pdf'
        with open(filename, 'wb') as f:
            f.write(pdf_content)
        print(f"✅ PDF con marcadores específicos guardado como '{filename}' ({len(pdf_content)} bytes)")
    except Exception as e:
        print(f"❌ Error al generar PDF con marcadores específicos: {e}")
    
    print("\n📝 Generando PDFs con coordenadas más precisas...")
    try:
        generar_pdf_con_coordenadas_precisas()
        print("✅ PDFs con coordenadas precisas generados correctamente")
    except Exception as e:
        print(f"❌ Error al generar PDFs con coordenadas precisas: {e}")
    
    print("\n📋 INSTRUCCIONES DETALLADAS:")
    print("1. Abre 'marcadores_especificos.pdf' para ver marcadores por campo")
    print("2. Abre los PDFs 'ajuste_preciso_config_1.pdf' hasta 'config_5.pdf'")
    print("3. Identifica qué configuración tiene los datos mejor posicionados")
    print("4. Dime específicamente:")
    print("   - ¿Qué configuración funciona mejor? (1, 2, 3, 4, o 5)")
    print("   - ¿Qué campos están bien y cuáles necesitan ajuste?")
    print("   - ¿Necesitas coordenadas específicas diferentes?")
    print("5. Con esa información ajustaré las coordenadas finales")
