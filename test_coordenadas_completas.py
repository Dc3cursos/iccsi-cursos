#!/usr/bin/env python
"""
Test completo de todas las coordenadas configuradas
Verifica que el PDF se genere correctamente con todos los campos
"""

import os
import sys
import django
from datetime import date

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccsi.settings')
django.setup()

from iccsi.cursos.views import generar_pdf_con_plantilla, generar_pdf_con_caracteres_individuales
from iccsi.cursos.models import PlantillaDC3, Organizacion

def test_coordenadas_completas():
    """Test completo de todas las coordenadas configuradas"""
    
    print("🧪 INICIANDO TEST COMPLETO DE COORDENADAS")
    print("=" * 50)
    
    # Datos de prueba
    datos_prueba = {
        'nombres': 'FERNANDO AGUILA MENDIETA',
        'curp': 'AUMF970410HDFGNR02',
        'puesto': 'ADMINISTRADOR',
        'nombre_curso': 'CURSO DE CAPACITACION',
        'horas_curso': '40',
        'instructor': 'DR. JUAN PEREZ',
        'nombre_empresa': 'FRATERNIDAD MIGRATORIA',
        'rfc_empresa': 'ADMINITRACION',
        'representante_legal': 'LIC. MARIA GONZALEZ',
        'representante_trabajadores': 'ING. CARLOS RODRIGUEZ',
        'fecha_inicio': date(2025, 8, 16),
        'fecha_fin': date(2025, 8, 16)
    }
    
    # Coordenadas configuradas (las que proporcionaste)
    coordenadas_configuradas = {
        'nombres': (225, 620),
        'curp': (43, 593),
        'puesto': (77, 578),
        'nombre_curso': (112, 450),
        'horas_curso': (54, 416),
        'instructor': (50, 302),
        'nombre_empresa': (200, 525),
        'rfc_empresa': (43, 496),
        'representante_legal': (225, 302),
        'representante_trabajadores': (400, 302),
        'fecha_inicio': (257, 416),
        'fecha_fin': (427, 416)
    }
    
        # Coordenadas para caracteres individuales (solo las que tienen valores numéricos)
    coordenadas_caracteres = {
            # CURP (18 caracteres)
            'curp_0': (43, 593), 'curp_1': (58, 593), 'curp_2': (72, 593), 'curp_3': (88, 593),
            'curp_4': (102, 593), 'curp_5': (117, 593), 'curp_6': (132, 593), 'curp_7': (145, 593),
            'curp_8': (158, 593), 'curp_9': (172, 593), 'curp_10': (187, 593), 'curp_11': (201, 593),
            'curp_12': (217, 593), 'curp_13': (233, 593), 'curp_14': (250, 593), 'curp_15': (265, 593),
            'curp_16': (279, 593), 'curp_17': (297, 593),
            
            # RFC (13 caracteres)
            'rfc_0': (45, 496), 'rfc_1': (58, 496), 'rfc_2': (72, 496), 'rfc_3': (90, 496),
            'rfc_4': (118, 496), 'rfc_5': (132, 496), 'rfc_6': (144, 496), 'rfc_7': (157, 496),
            'rfc_8': (172, 496), 'rfc_9': (186, 496), 'rfc_10': (217, 496), 'rfc_11': (233, 496),
            'rfc_12': (250, 496),
            
            # Fecha Inicio (solo las posiciones con coordenadas válidas)
            'fecha_ini_0': (260, 416), 'fecha_ini_1': (277, 416), 'fecha_ini_2': (292, 416),
            'fecha_ini_3': (308, 416), 'fecha_ini_5': (327, 416), 'fecha_ini_6': (347, 416),
            'fecha_ini_8': (368, 416), 'fecha_ini_9': (390, 416),
            
            # Fecha Fin (solo las posiciones con coordenadas válidas)
            'fecha_fin_0': (431, 416), 'fecha_fin_1': (450, 416), 'fecha_fin_2': (470, 416),
            'fecha_fin_3': (487, 416), 'fecha_fin_5': (510, 416), 'fecha_fin_6': (530, 416),
            'fecha_fin_8': (550, 416), 'fecha_fin_9': (570, 416)
        }
    
    try:
        # Obtener la plantilla
        organizacion = Organizacion.objects.get(nombre='Fraternidad Migratoria')
        plantilla = PlantillaDC3.objects.get(organizacion=organizacion)
        
        print(f"✅ Plantilla encontrada: {plantilla.nombre}")
        print(f"📁 Archivo: {plantilla.archivo}")
        
        # Test 1: Generar PDF con coordenadas de campos completos
        print("\n📋 TEST 1: Generando PDF con coordenadas de campos completos...")
        pdf_content = generar_pdf_con_plantilla(
            datos_prueba, 
            plantilla.id, 
            coordenadas_personalizadas=coordenadas_configuradas
        )
        
        if pdf_content:
            with open('test_campos_completos.pdf', 'wb') as f:
                f.write(pdf_content)
            print(f"✅ PDF generado: test_campos_completos.pdf ({len(pdf_content)} bytes)")
        else:
            print("❌ Error al generar PDF con campos completos")
            return False
        
        # Test 2: Generar PDF con caracteres individuales
        print("\n🔤 TEST 2: Generando PDF con caracteres individuales...")
        pdf_content = generar_pdf_con_caracteres_individuales(
            datos_prueba,
            plantilla.id,
            coordenadas_caracteres
        )
        
        if pdf_content:
            with open('test_caracteres_individuales.pdf', 'wb') as f:
                f.write(pdf_content)
            print(f"✅ PDF generado: test_caracteres_individuales.pdf ({len(pdf_content)} bytes)")
        else:
            print("❌ Error al generar PDF con caracteres individuales")
            return False
        
        # Verificar archivos generados
        print("\n📊 RESUMEN DE ARCHIVOS GENERADOS:")
        archivos = ['test_campos_completos.pdf', 'test_caracteres_individuales.pdf']
        for archivo in archivos:
            if os.path.exists(archivo):
                size = os.path.getsize(archivo)
                print(f"✅ {archivo}: {size:,} bytes")
            else:
                print(f"❌ {archivo}: No encontrado")
        
        print("\n🎯 COORDENADAS APLICADAS:")
        print("Campos completos:")
        for campo, coords in coordenadas_configuradas.items():
            print(f"   {campo}: ({coords[0]}, {coords[1]})")
        
        print("\nCaracteres individuales:")
        print(f"   CURP: 18 caracteres con coordenadas específicas")
        print(f"   RFC: 13 caracteres con coordenadas específicas")
        print(f"   Fechas: formato YYYYMMDD sin barras")
        
        print("\n✅ TEST COMPLETO EXITOSO")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"❌ Error durante el test: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_coordenadas_completas()
    if success:
        print("\n🎉 ¡Todos los tests pasaron! Los PDFs se generaron correctamente.")
        print("📁 Revisa los archivos generados:")
        print("   - test_campos_completos.pdf")
        print("   - test_caracteres_individuales.pdf")
    else:
        print("\n💥 Algunos tests fallaron. Revisa los errores arriba.")
    
    sys.exit(0 if success else 1)
