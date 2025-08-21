#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccsi.settings')
django.setup()

from datetime import date
from iccsi.cursos.views import generar_pdf_con_plantilla

def test_coordenadas_finales():
    """Prueba las coordenadas finales actualizadas"""
    
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
        # Generar PDF con coordenadas actualizadas
        pdf_content = generar_pdf_con_plantilla(data, 10)
        
        # Guardar el PDF para verificar
        with open('test_coordenadas_finales.pdf', 'wb') as f:
            f.write(pdf_content)
        
        print(f"✅ PDF generado exitosamente: {len(pdf_content)} bytes")
        print(f"📄 Archivo guardado como: test_coordenadas_finales.pdf")
        print(f"🎯 Coordenadas aplicadas:")
        print(f"   - Nombres: (200, 650)")
        print(f"   - CURP: (200, 620)")
        print(f"   - Puesto: (200, 590)")
        print(f"   - Curso: (200, 530)")
        print(f"   - Horas: (200, 500)")
        print(f"   - Empresa: (200, 560)")
        print(f"   - RFC: (200, 470)")
        print(f"   - Representantes: (200, 470) y (200, 440)")
        print(f"   - Fechas: (200, 410) y (200, 380)")
        print(f"   - Instructor: (200, 410)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al generar PDF: {e}")
        return False

if __name__ == "__main__":
    test_coordenadas_finales()
