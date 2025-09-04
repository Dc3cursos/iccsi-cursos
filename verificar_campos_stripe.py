#!/usr/bin/env python
"""
Script para verificar que los campos de Stripe estén presentes en la base de datos
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccsi.iccsi.settings')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line

def verificar_campos_stripe():
    """Verifica que los campos de Stripe estén presentes en la tabla cursos_pago"""
    with connection.cursor() as cursor:
        # Obtener información de las columnas de la tabla cursos_pago
        cursor.execute("PRAGMA table_info(cursos_pago)")
        columns = cursor.fetchall()
        
        print("🔍 Verificando campos de Stripe en la tabla cursos_pago...")
        print(f"📋 Columnas encontradas: {len(columns)}")
        
        # Buscar campos de Stripe
        campos_stripe = [
            'stripe_payment_intent_id',
            'stripe_charge_id', 
            'stripe_status',
            'stripe_client_secret'
        ]
        
        campos_encontrados = []
        for column in columns:
            column_name = column[1]  # El nombre de la columna está en el índice 1
            if column_name in campos_stripe:
                campos_encontrados.append(column_name)
                print(f"✅ Campo encontrado: {column_name}")
        
        # Verificar si faltan campos
        campos_faltantes = [campo for campo in campos_stripe if campo not in campos_encontrados]
        
        if campos_faltantes:
            print(f"❌ Campos faltantes: {campos_faltantes}")
            print("🔧 Intentando agregar campos faltantes...")
            
            for campo in campos_faltantes:
                try:
                    if campo == 'stripe_payment_intent_id':
                        cursor.execute("ALTER TABLE cursos_pago ADD COLUMN stripe_payment_intent_id varchar(255)")
                    elif campo == 'stripe_charge_id':
                        cursor.execute("ALTER TABLE cursos_pago ADD COLUMN stripe_charge_id varchar(255)")
                    elif campo == 'stripe_status':
                        cursor.execute("ALTER TABLE cursos_pago ADD COLUMN stripe_status varchar(50)")
                    elif campo == 'stripe_client_secret':
                        cursor.execute("ALTER TABLE cursos_pago ADD COLUMN stripe_client_secret varchar(255)")
                    
                    print(f"✅ Campo {campo} agregado exitosamente")
                except Exception as e:
                    print(f"❌ Error al agregar campo {campo}: {e}")
        else:
            print("🎉 Todos los campos de Stripe están presentes")
        
        # Mostrar todas las columnas
        print("\n📋 Todas las columnas de la tabla cursos_pago:")
        for column in columns:
            print(f"  - {column[1]} ({column[2]})")

if __name__ == '__main__':
    verificar_campos_stripe()
