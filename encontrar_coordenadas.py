#!/usr/bin/env python
"""
Script para encontrar las coordenadas exactas de la plantilla PDF
Genera PDFs de prueba con marcadores visibles para identificar las posiciones correctas
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

def generar_pdf_con_marcadores():
    """Genera un PDF con marcadores visibles para encontrar coordenadas"""
    
    from PyPDF2 import PdfReader, PdfWriter
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.colors import black, red, blue
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
        
        # Crear un PDF temporal con marcadores
        data_pdf = io.BytesIO()
        c = canvas.Canvas(data_pdf)
        
        # Configurar fuentes
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(red)
        
        # Generar marcadores en diferentes posiciones
        posiciones_test = [
            # Posiciones para nombre (parte superior)
            (200, 700, "NOMBRE AQUI"),
            (250, 700, "NOMBRE AQUI"),
            (300, 700, "NOMBRE AQUI"),
            (350, 700, "NOMBRE AQUI"),
            (400, 700, "NOMBRE AQUI"),
            
            # Posiciones para CURP
            (200, 650, "CURP AQUI"),
            (250, 650, "CURP AQUI"),
            (300, 650, "CURP AQUI"),
            (350, 650, "CURP AQUI"),
            (400, 650, "CURP AQUI"),
            
            # Posiciones para puesto
            (200, 600, "PUESTO AQUI"),
            (250, 600, "PUESTO AQUI"),
            (300, 600, "PUESTO AQUI"),
            (350, 600, "PUESTO AQUI"),
            (400, 600, "PUESTO AQUI"),
            
            # Posiciones para curso
            (200, 550, "CURSO AQUI"),
            (250, 550, "CURSO AQUI"),
            (300, 550, "CURSO AQUI"),
            (350, 550, "CURSO AQUI"),
            (400, 550, "CURSO AQUI"),
            
            # Posiciones para empresa
            (200, 500, "EMPRESA AQUI"),
            (250, 500, "EMPRESA AQUI"),
            (300, 500, "EMPRESA AQUI"),
            (350, 500, "EMPRESA AQUI"),
            (400, 500, "EMPRESA AQUI"),
            
            # Posiciones para instructor
            (200, 450, "INSTRUCTOR AQUI"),
            (250, 450, "INSTRUCTOR AQUI"),
            (300, 450, "INSTRUCTOR AQUI"),
            (350, 450, "INSTRUCTOR AQUI"),
            (400, 450, "INSTRUCTOR AQUI"),
            
            # Posiciones para fechas
            (200, 400, "FECHA AQUI"),
            (250, 400, "FECHA AQUI"),
            (300, 400, "FECHA AQUI"),
            (350, 400, "FECHA AQUI"),
            (400, 400, "FECHA AQUI"),
        ]
        
        # Dibujar marcadores
        for x, y, texto in posiciones_test:
            # Dibujar un círculo rojo en la posición
            c.setFillColor(red)
            c.circle(x, y, 3, fill=1)
            
            # Dibujar el texto
            c.setFillColor(blue)
            c.drawString(x + 10, y - 5, texto)
            
            # Dibujar coordenadas
            c.setFillColor(black)
            c.setFont("Helvetica", 8)
            c.drawString(x + 10, y - 20, f"({x}, {y})")
        
        # Agregar instrucciones
        c.setFillColor(black)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, 750, "INSTRUCCIONES PARA ENCONTRAR COORDENADAS:")
        c.setFont("Helvetica", 10)
        c.drawString(50, 730, "1. Los círculos rojos marcan las posiciones de prueba")
        c.drawString(50, 715, "2. Los textos azules indican qué dato va en cada posición")
        c.drawString(50, 700, "3. Los números en negro son las coordenadas (X, Y)")
        c.drawString(50, 685, "4. Identifica qué marcador está en la posición correcta")
        c.drawString(50, 670, "5. Usa esas coordenadas en el sistema")
        
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

def generar_pdf_con_datos_reales():
    """Genera un PDF con datos reales en diferentes posiciones"""
    
    from PyPDF2 import PdfReader, PdfWriter
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.colors import black
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
        
        # Crear un nuevo PDF con los datos
        output = PdfWriter()
        
        # Crear un PDF temporal con los datos
        data_pdf = io.BytesIO()
        c = canvas.Canvas(data_pdf)
        
        # Configurar fuente
        c.setFont("Helvetica", 10)
        
        # Diferentes configuraciones de coordenadas para probar
        configuraciones = {
            'config_a': {
                'nombres': (150, 680),
                'curp': (150, 650),
                'puesto': (150, 620),
                'ocupacion': (150, 590),
                'nombre_curso': (150, 560),
                'horas_curso': (150, 530),
                'area_tematica': (150, 500),
                'nombre_empresa': (150, 470),
                'rfc_empresa': (150, 440),
                'representante_legal': (150, 410),
                'representante_trabajadores': (150, 380),
                'fecha_inicio': (150, 350),
                'fecha_fin': (150, 320),
                'instructor_nombre': (150, 290),
            },
            'config_b': {
                'nombres': (200, 680),
                'curp': (200, 650),
                'puesto': (200, 620),
                'ocupacion': (200, 590),
                'nombre_curso': (200, 560),
                'horas_curso': (200, 530),
                'area_tematica': (200, 500),
                'nombre_empresa': (200, 470),
                'rfc_empresa': (200, 440),
                'representante_legal': (200, 410),
                'representante_trabajadores': (200, 380),
                'fecha_inicio': (200, 350),
                'fecha_fin': (200, 320),
                'instructor_nombre': (200, 290),
            },
            'config_c': {
                'nombres': (250, 680),
                'curp': (250, 650),
                'puesto': (250, 620),
                'ocupacion': (250, 590),
                'nombre_curso': (250, 560),
                'horas_curso': (250, 530),
                'area_tematica': (250, 500),
                'nombre_empresa': (250, 470),
                'rfc_empresa': (250, 440),
                'representante_legal': (250, 410),
                'representante_trabajadores': (250, 380),
                'fecha_inicio': (250, 350),
                'fecha_fin': (250, 320),
                'instructor_nombre': (250, 290),
            }
        }
        
        # Generar PDF para cada configuración
        for config_name, posiciones in configuraciones.items():
            print(f"🧪 Generando PDF con {config_name}...")
            
            # Crear un nuevo canvas para cada configuración
            config_pdf = io.BytesIO()
            c_config = canvas.Canvas(config_pdf)
            c_config.setFont("Helvetica", 10)
            
            # Escribir los datos en el PDF
            for campo, (x, y) in posiciones.items():
                if campo in ['nombres', 'apellido_paterno', 'apellido_materno']:
                    # Combinar nombre completo en una sola línea
                    nombre_completo = f"{data.get('nombres', '')} {data.get('apellido_paterno', '')} {data.get('apellido_materno', '')}".strip()
                    if campo == 'nombres':  # Solo escribir una vez
                        c_config.drawString(x, y, nombre_completo)
                    continue
                elif campo in ['apellido_paterno', 'apellido_materno']:
                    continue  # Ya se manejó arriba
                else:
                    valor = data.get(campo, '')
                    if hasattr(valor, 'strftime'):  # Verificar si es una fecha
                        valor = valor.strftime('%d/%m/%Y')
                    c_config.drawString(x, y, str(valor))
            
            c_config.save()
            config_pdf.seek(0)
            
            # Combinar con la plantilla
            config_reader = PdfReader(config_pdf)
            config_page = config_reader.pages[0]
            
            # Crear una copia de la plantilla para esta configuración
            template_copy = template_page
            template_copy.merge_page(config_page)
            
            # Agregar a un nuevo writer
            output_config = PdfWriter()
            output_config.add_page(template_copy)
            
            # Generar el PDF final
            result_pdf = io.BytesIO()
            output_config.write(result_pdf)
            result_pdf.seek(0)
            
            # Guardar el PDF
            filename = f'test_datos_{config_name}.pdf'
            with open(filename, 'wb') as f:
                f.write(result_pdf.getvalue())
            print(f"✅ PDF guardado como '{filename}' ({len(result_pdf.getvalue())} bytes)")

if __name__ == "__main__":
    print("🔍 Generando PDF con marcadores para encontrar coordenadas...")
    try:
        pdf_content = generar_pdf_con_marcadores()
        filename = 'coordenadas_marcadores.pdf'
        with open(filename, 'wb') as f:
            f.write(pdf_content)
        print(f"✅ PDF con marcadores guardado como '{filename}' ({len(pdf_content)} bytes)")
    except Exception as e:
        print(f"❌ Error al generar PDF con marcadores: {e}")
    
    print("\n📝 Generando PDFs con datos reales en diferentes posiciones...")
    try:
        generar_pdf_con_datos_reales()
        print("✅ PDFs con datos reales generados correctamente")
    except Exception as e:
        print(f"❌ Error al generar PDFs con datos reales: {e}")
    
    print("\n📋 INSTRUCCIONES:")
    print("1. Abre 'coordenadas_marcadores.pdf' para ver las posiciones de prueba")
    print("2. Abre los PDFs 'test_datos_config_a.pdf', 'test_datos_config_b.pdf', etc.")
    print("3. Compara dónde están mejor posicionados los datos")
    print("4. Dime qué configuración funciona mejor o las coordenadas específicas que necesitas")
