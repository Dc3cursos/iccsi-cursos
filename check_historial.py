#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccsi.settings')
django.setup()

from iccsi.cursos.models import HistorialCertificadoDC3

print("🔍 VERIFICANDO HISTORIAL DE CERTIFICADOS")
print("=" * 50)

certs = HistorialCertificadoDC3.objects.all()
print(f"Total certificados: {certs.count()}")

for cert in certs:
    print(f"Folio: {cert.folio}")
    print(f"Código: {cert.codigo_verificacion}")
    print(f"Alumno: {cert.nombre_completo_alumno}")
    print(f"Fecha: {cert.fecha_generacion}")
    print("-" * 30)

print("✅ Verificación completada")
