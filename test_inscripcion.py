#!/usr/bin/env python
"""
Script de prueba para verificar el sistema de inscripción y certificados DC-3
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccsi.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()
from iccsi.cursos.models import Curso, Inscripcion, CertificadoDC3

def test_sistema_inscripcion():
    print("=== PRUEBA DEL SISTEMA DE INSCRIPCIÓN ===")
    
    # 1. Verificar usuarios
    print("\n1. Verificando usuarios...")
    usuarios = User.objects.all()
    print(f"Usuarios encontrados: {usuarios.count()}")
    for usuario in usuarios:
        print(f"  - {usuario.username} ({usuario.first_name} {usuario.last_name})")
    
    # 2. Verificar cursos
    print("\n2. Verificando cursos...")
    cursos = Curso.objects.all()
    print(f"Cursos encontrados: {cursos.count()}")
    for curso in cursos:
        print(f"  - {curso.nombre} ({curso.duracion_horas} horas) - Profesor: {curso.profesor.username}")
    
    # 3. Verificar inscripciones
    print("\n3. Verificando inscripciones...")
    inscripciones = Inscripcion.objects.all()
    print(f"Inscripciones encontradas: {inscripciones.count()}")
    for inscripcion in inscripciones:
        print(f"  - {inscripcion.alumno.username} -> {inscripcion.curso.nombre} ({inscripcion.fecha_inscripcion})")
    
    # 4. Verificar certificados
    print("\n4. Verificando certificados...")
    certificados = CertificadoDC3.objects.all()
    print(f"Certificados encontrados: {certificados.count()}")
    for certificado in certificados:
        print(f"  - {certificado.nombre_completo} -> {certificado.inscripcion.curso.nombre} (PDF: {certificado.archivo_pdf.name if certificado.archivo_pdf else 'No'})")
    
    # 5. Verificar inscripciones por usuario específico
    print("\n5. Verificando inscripciones por usuario...")
    for usuario in usuarios:
        inscripciones_usuario = Inscripcion.objects.filter(alumno=usuario)
        print(f"  {usuario.username}: {inscripciones_usuario.count()} inscripciones")
        for inscripcion in inscripciones_usuario:
            print(f"    - {inscripcion.curso.nombre}")
            if hasattr(inscripcion, 'certificado') and inscripcion.certificado:
                print(f"      Certificado: {inscripcion.certificado.archivo_pdf.name if inscripcion.certificado.archivo_pdf else 'Sin PDF'}")
            else:
                print(f"      Certificado: No generado")

if __name__ == "__main__":
    test_sistema_inscripcion()
