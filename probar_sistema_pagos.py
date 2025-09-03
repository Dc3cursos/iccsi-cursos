#!/usr/bin/env python
"""
Script para probar el sistema de pagos
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccsi.iccsi.settings')
django.setup()

from django.contrib.auth import get_user_model
from iccsi.cursos.models import Curso, Inscripcion, Pago, CostoCurso
from django.utils import timezone

User = get_user_model()

def probar_sistema_pagos():
    """Prueba el sistema de pagos"""
    print("🧪 Probando sistema de pagos...")
    
    # Crear un usuario de prueba
    try:
        usuario = User.objects.get(username='test_user')
        print("✅ Usuario de prueba encontrado")
    except User.DoesNotExist:
        usuario = User.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='test123',
            first_name='Usuario',
            last_name='Prueba',
            rol='alumno'
        )
        print("✅ Usuario de prueba creado")
    
    # Obtener un curso
    try:
        curso = Curso.objects.first()
        if not curso:
            print("❌ No hay cursos en la base de datos")
            return
        print(f"✅ Curso encontrado: {curso.nombre}")
    except Exception as e:
        print(f"❌ Error al obtener curso: {e}")
        return
    
    # Crear o obtener costo del curso
    try:
        costo, created = CostoCurso.objects.get_or_create(
            curso=curso,
            defaults={'precio': 380.00, 'moneda': 'MXN'}
        )
        if created:
            print("✅ Costo del curso creado")
        else:
            print("✅ Costo del curso encontrado")
    except Exception as e:
        print(f"❌ Error al crear/obtener costo: {e}")
        return
    
    # Crear inscripción
    try:
        inscripcion, created = Inscripcion.objects.get_or_create(
            alumno=usuario,
            curso=curso,
            defaults={'fecha_inscripcion': timezone.now()}
        )
        if created:
            print("✅ Inscripción creada")
        else:
            print("✅ Inscripción encontrada")
    except Exception as e:
        print(f"❌ Error al crear inscripción: {e}")
        return
    
    # Crear pago
    try:
        pago, created = Pago.objects.get_or_create(
            inscripcion=inscripcion,
            defaults={
                'monto': costo.precio,
                'metodo_pago': 'tarjeta',
                'estado': 'completado',
                'fecha_pago': timezone.now(),
                'stripe_payment_intent_id': 'pi_test_123456789',
                'stripe_status': 'succeeded'
            }
        )
        if created:
            print("✅ Pago creado")
        else:
            print("✅ Pago encontrado")
    except Exception as e:
        print(f"❌ Error al crear pago: {e}")
        return
    
    # Probar acceso a campos de Stripe
    try:
        print(f"🔍 Verificando campos de Stripe:")
        print(f"  - stripe_payment_intent_id: {pago.stripe_payment_intent_id}")
        print(f"  - stripe_status: {pago.stripe_status}")
        print(f"  - stripe_charge_id: {pago.stripe_charge_id}")
        print(f"  - stripe_client_secret: {pago.stripe_client_secret}")
        print("✅ Campos de Stripe accesibles")
    except Exception as e:
        print(f"❌ Error al acceder a campos de Stripe: {e}")
        return
    
    # Probar la relación Inscripcion -> Pago
    try:
        pago_desde_inscripcion = inscripcion.pago
        print(f"✅ Relación Inscripcion -> Pago funciona: {pago_desde_inscripcion}")
    except Exception as e:
        print(f"❌ Error en relación Inscripcion -> Pago: {e}")
        return
    
    # Probar la propiedad es_pagado
    try:
        es_pagado = pago.es_pagado
        print(f"✅ Propiedad es_pagado funciona: {es_pagado}")
    except Exception as e:
        print(f"❌ Error en propiedad es_pagado: {e}")
        return
    
    print("\n🎉 ¡Sistema de pagos funcionando correctamente!")

if __name__ == '__main__':
    probar_sistema_pagos()
