#!/usr/bin/env python
import os
import django
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccsi.iccsi.settings')
django.setup()

def configurar_credenciales_sociales():
    print("🔧 Configurando credenciales de autenticación social...")
    
    # Obtener o crear el sitio
    site, created = Site.objects.get_or_create(
        id=1,
        defaults={
            'domain': '127.0.0.1:8000',
            'name': 'Instituto Capacitación IC'
        }
    )
    if created:
        print(f"✅ Sitio creado: {site.name} ({site.domain})")
    else:
        print(f"✅ Sitio existente: {site.name} ({site.domain})")
    
    # Configurar Google OAuth2
    google_app, created = SocialApp.objects.get_or_create(
        provider='google',
        defaults={
            'name': 'Google',
            'client_id': '123456789-abcdefghijklmnop.apps.googleusercontent.com',
            'secret': 'GOCSPX-abcdefghijklmnopqrstuvwxyz',
            'key': ''
        }
    )
    if created:
        google_app.sites.add(site)
        print("✅ Aplicación Google creada con credenciales de prueba")
    else:
        print("✅ Aplicación Google ya existe")
    
    # Configurar Microsoft OAuth2
    microsoft_app, created = SocialApp.objects.get_or_create(
        provider='microsoft',
        defaults={
            'name': 'Microsoft',
            'client_id': '12345678-1234-1234-1234-123456789012',
            'secret': 'abcdefghijklmnopqrstuvwxyz123456',
            'key': ''
        }
    )
    if created:
        microsoft_app.sites.add(site)
        print("✅ Aplicación Microsoft creada con credenciales de prueba")
    else:
        print("✅ Aplicación Microsoft ya existe")
    
    # Configurar Apple OAuth2
    apple_app, created = SocialApp.objects.get_or_create(
        provider='apple',
        defaults={
            'name': 'Apple',
            'client_id': 'com.iccsi.academia',
            'secret': '-----BEGIN PRIVATE KEY-----\nMIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQg...\n-----END PRIVATE KEY-----',
            'key': 'ABC123DEF456'
        }
    )
    if created:
        apple_app.sites.add(site)
        print("✅ Aplicación Apple creada con credenciales de prueba")
    else:
        print("✅ Aplicación Apple ya existe")
    
    print("\n🎉 ¡Configuración completada!")
    print("\n📋 Credenciales configuradas:")
    print("   • Google: Credenciales de prueba configuradas")
    print("   • Microsoft: Credenciales de prueba configuradas") 
    print("   • Apple: Credenciales de prueba configuradas")
    print("\n⚠️  NOTA: Estas son credenciales de prueba.")
    print("   Para producción, necesitas obtener credenciales reales de:")
    print("   • Google: https://console.developers.google.com/")
    print("   • Microsoft: https://portal.azure.com/")
    print("   • Apple: https://developer.apple.com/")

if __name__ == '__main__':
    configurar_credenciales_sociales()
