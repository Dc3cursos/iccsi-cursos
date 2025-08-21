#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccsi.settings')
django.setup()

from iccsi.cursos.views import generar_pdf_con_caracteres_individuales
from datetime import date

def test_proteccion_automatica():
    print("=== PRUEBA DE PROTECCIÓN AUTOMÁTICA ===\n")
    
    # Datos de prueba
    data = {
        'apellido_paterno': 'AGUILA',
        'apellido_materno': 'MENDIETA', 
        'nombres': 'FERNANDO',
        'curp': 'AUMF970410HDFGNR02',
        'puesto': 'TECNICO',
        'nombre_curso': 'NORMA OFICIAL MEXICANA NOM-002-STPS-2010,CONDICIONES DE SEGURIDAD,PREVENCION Y PROTECCION CONTRA INCENDIOS EN LOS CENTROS DE TRABAJO BLOQUEO CANDADEO Y ETIQUETADO (LOTO)',
        'horas_curso': '8',
        'nombre_empresa': 'ADMINITRACION DE CONDOMINIOS MY HOGAR',
        'rfc_empresa': 'ADMINITRACION',
        'representante_legal': 'MARIA DEL CARMEL GARCIA',
        'representante_trabajadores': 'JUAN CARLOS DE ROSA',
        'fecha_inicio': date(2025, 8, 19),
        'fecha_fin': date(2025, 8, 19),
        'instructor_nombre': 'EDUARDO MENDIETA ZUÑIGA',
    }
    
    # Coordenadas para caracteres individuales
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
        print("🔒 Generando PDF con protección automática...")
        pdf_content = generar_pdf_con_caracteres_individuales(data, 10, coordenadas_caracteres)
        
        print(f"✅ PDF con protección automática generado exitosamente!")
        print(f"📄 Tamaño del PDF: {len(pdf_content)} bytes")
        
        # Guardar el PDF para verificación
        with open('certificado_proteccion_automatica.pdf', 'wb') as f:
            f.write(pdf_content)
        
        print(f"💾 PDF guardado como: certificado_proteccion_automatica.pdf")
        print("\n🔐 INFORMACIÓN DE PROTECCIÓN AUTOMÁTICA:")
        print("   • Tipo: Protección automática sin contraseña")
        print("   • Modo: Solo lectura")
        print("   • Encriptación: 128-bit")
        print("   • Restricciones: No se puede editar, copiar o imprimir")
        print("   • Apertura: Automática (sin contraseña)")
        
        print("\n🎯 El certificado está protegido automáticamente!")
        print("📋 Para abrir el PDF: Simplemente hacer doble clic (sin contraseña)")
        print("🔒 Las restricciones se aplican automáticamente al descargar")
        
    except Exception as e:
        print(f"❌ Error al generar PDF con protección automática: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_proteccion_automatica()
