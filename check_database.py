#!/usr/bin/env python
"""
Script para verificar si el certificado se guardó en la base de datos
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccsi.settings')
django.setup()

from iccsi.cursos.models import HistorialCertificadoDC3

def check_database():
    """Verificar certificados en la base de datos"""
    
    print("🔍 VERIFICANDO BASE DE DATOS")
    print("=" * 50)
    
    # Buscar todos los certificados
    certificados = HistorialCertificadoDC3.objects.all().order_by('-fecha_generacion')
    
    print(f"📊 Total de certificados en BD: {certificados.count()}")
    
    if certificados.exists():
        print("\n📋 Últimos 5 certificados:")
        for i, cert in enumerate(certificados[:5]):
            print(f"\n{i+1}. Certificado:")
            print(f"   Folio: {cert.folio}")
            print(f"   Alumno: {cert.nombre_completo_alumno}")
            print(f"   Empresa: {cert.nombre_empresa}")
            print(f"   Curso: {cert.nombre_curso}")
            print(f"   Fecha: {cert.fecha_generacion}")
            print(f"   Código: {cert.codigo_verificacion}")
    else:
        print("❌ No hay certificados en la base de datos")
    
    # Buscar específicamente el certificado de AGUILA MENDIETA FERNANDO
    print("\n🔍 Buscando certificado específico:")
    cert_especifico = certificados.filter(
        nombre_completo_alumno__icontains='AGUILA MENDIETA FERNANDO'
    ).first()
    
    if cert_especifico:
        print(f"✅ Encontrado:")
        print(f"   Folio: {cert_especifico.folio}")
        print(f"   Alumno: {cert_especifico.nombre_completo_alumno}")
        print(f"   Empresa: {cert_especifico.nombre_empresa}")
        print(f"   Curso: {cert_especifico.nombre_curso}")
        print(f"   Fecha: {cert_especifico.fecha_generacion}")
    else:
        print("❌ No se encontró el certificado específico")

if __name__ == '__main__':
    check_database()
