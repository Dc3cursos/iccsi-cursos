#!/usr/bin/env python
"""
Script de debug para verificar la extracción de folio del PDF más reciente
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccsi.settings')
django.setup()

from PyPDF2 import PdfReader
import re
import io
import glob

def debug_latest_pdf():
    """Debug del PDF más reciente"""
    
    print("🔍 DEBUG: Extracción de folio del PDF más reciente")
    print("=" * 60)
    
    # Buscar el PDF más reciente en la carpeta de descargas
    downloads_path = os.path.expanduser("~/Downloads")
    pdf_files = glob.glob(os.path.join(downloads_path, "DC3_*.pdf"))
    
    if not pdf_files:
        print("❌ No se encontraron PDFs DC3 en la carpeta de descargas")
        return
    
    # Tomar el más reciente
    latest_pdf = max(pdf_files, key=os.path.getctime)
    print(f"📄 PDF encontrado: {latest_pdf}")
    print(f"📄 Fecha de creación: {os.path.getctime(latest_pdf)}")
    
    try:
        # Leer el PDF
        with open(latest_pdf, 'rb') as file:
            pdf_content = file.read()
        
        print(f"📄 Tamaño del PDF: {len(pdf_content)} bytes")
        
        # Leer el PDF con PyPDF2
        pdf_reader = PdfReader(io.BytesIO(pdf_content))
        content_data = b''
        
        print(f"📄 Número de páginas: {len(pdf_reader.pages)}")
        
        # Extraer contenido de todas las páginas
        for i, page in enumerate(pdf_reader.pages):
            print(f"📄 Procesando página {i+1}")
            if '/Contents' in page:
                contents = page['/Contents']
                if hasattr(contents, 'get_data'):
                    page_data = contents.get_data()
                    content_data += page_data
                    print(f"📄 Contenido de página {i+1}: {len(page_data)} bytes")
                else:
                    print(f"⚠️ No se pudo obtener datos de página {i+1}")
            else:
                print(f"⚠️ Página {i+1} no tiene contenido")
        
        # Convertir a string para búsqueda
        content_str = content_data.decode('utf-8', errors='ignore')
        
        print(f"📄 Contenido total extraído: {len(content_str)} caracteres")
        
        # Buscar folio con diferentes patrones
        patrones_folio = [
            r'FOLIO:\s*(DC3-\d{4}-\d{5})',
            r'(DC3-\d{4}-\d{5})',
            r'FOLIO:\s*([A-Z0-9-]+)',
            r'([A-Z0-9-]{10,})',  # Cualquier código largo
        ]
        
        print("\n🔍 Buscando folio con patrones:")
        folio_encontrado = None
        
        for i, patron in enumerate(patrones_folio):
            matches = re.findall(patron, content_str)
            print(f"Patrón {i+1}: {patron}")
            print(f"Coincidencias encontradas: {matches}")
            if matches and not folio_encontrado:
                folio_encontrado = matches[0]
                print(f"✅ Folio encontrado: {matches[0]}")
        
        if not folio_encontrado:
            print("❌ No se encontró ningún folio")
            
            # Buscar cualquier texto que contenga "FOLIO"
            folio_matches = re.findall(r'FOLIO[:\s]*([^\s\n]+)', content_str, re.IGNORECASE)
            if folio_matches:
                print(f"🔍 Textos con 'FOLIO' encontrados: {folio_matches}")
            
            # Mostrar fragmentos del contenido que contengan "FOLIO"
            folio_lines = [line for line in content_str.split('\n') if 'FOLIO' in line.upper()]
            if folio_lines:
                print(f"🔍 Líneas con 'FOLIO': {folio_lines[:5]}")
        
        # Verificar en la base de datos
        from iccsi.cursos.models import HistorialCertificadoDC3
        certificados = HistorialCertificadoDC3.objects.all().order_by('-fecha_generacion')
        print(f"\n📊 Total de certificados en BD: {certificados.count()}")
        
        if certificados.exists():
            ultimo_cert = certificados.first()
            print(f"📋 Último certificado en BD:")
            print(f"   Folio: {ultimo_cert.folio}")
            print(f"   Alumno: {ultimo_cert.nombre_completo_alumno}")
            print(f"   Fecha: {ultimo_cert.fecha_generacion}")
            
            if folio_encontrado and folio_encontrado == ultimo_cert.folio:
                print("✅ ¡COINCIDENCIA! El folio del PDF coincide con el de la BD")
            else:
                print("❌ NO COINCIDE - El folio del PDF no coincide con el de la BD")
        
        return folio_encontrado
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == '__main__':
    debug_latest_pdf()
