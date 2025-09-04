#!/usr/bin/env python3
"""
Script para configurar automáticamente el proyecto ICCSI para despliegue
"""
import os
import secrets
import subprocess
import sys
from pathlib import Path

def generate_secret_key():
    """Genera una nueva clave secreta para Django"""
    return secrets.token_urlsafe(50)

def create_env_file():
    """Crea el archivo .env con configuraciones por defecto"""
    env_content = f"""# Configuración de Django
SECRET_KEY={generate_secret_key()}
DEBUG=False

# Configuración de base de datos
DATABASE_NAME=iccsi
DATABASE_USER=postgres
DATABASE_PASSWORD=tu_password_aqui
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Configuración de Stripe
STRIPE_PUBLISHABLE_KEY=pk_test_tu_clave_publica_aqui
STRIPE_SECRET_KEY=sk_test_tu_clave_secreta_aqui
STRIPE_WEBHOOK_SECRET=whsec_tu_webhook_secret_aqui

# Configuración de CORS
CORS_ALLOWED_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com
"""
    
    env_path = Path('.env')
    if not env_path.exists():
        with open(env_path, 'w') as f:
            f.write(env_content)
        print("✅ Archivo .env creado exitosamente")
    else:
        print("ℹ️  El archivo .env ya existe")

def install_dependencies():
    """Instala las dependencias del proyecto"""
    print("📦 Instalando dependencias...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("✅ Dependencias instaladas exitosamente")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False
    return True

def run_migrations():
    """Ejecuta las migraciones de la base de datos"""
    print("🗄️  Ejecutando migraciones...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'makemigrations'], check=True)
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        print("✅ Migraciones ejecutadas exitosamente")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando migraciones: {e}")
        return False
    return True

def create_superuser():
    """Crea un superusuario por defecto"""
    print("👤 Creando superusuario...")
    try:
        # Crear superusuario con credenciales por defecto
        subprocess.run([
            sys.executable, 'manage.py', 'createsuperuser',
            '--username', 'admin',
            '--email', 'admin@iccsi.com',
            '--noinput'
        ], check=True)
        
        # Cambiar contraseña del superusuario
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.get(username='admin')
        user.set_password('admin123')
        user.save()
        
        print("✅ Superusuario creado exitosamente")
        print("   Usuario: admin")
        print("   Contraseña: admin123")
        print("   ⚠️  Cambia la contraseña después del primer login")
    except Exception as e:
        print(f"❌ Error creando superusuario: {e}")
        return False
    return True

def collect_static():
    """Recopila archivos estáticos"""
    print("📁 Recopilando archivos estáticos...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], check=True)
        print("✅ Archivos estáticos recopilados")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error recopilando archivos estáticos: {e}")
        return False
    return True

def main():
    """Función principal del script"""
    print("🚀 Configurando ICCSI para despliegue...")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not Path('manage.py').exists():
        print("❌ Error: No se encontró manage.py. Ejecuta este script desde el directorio raíz del proyecto.")
        return
    
    # Crear archivo .env
    create_env_file()
    
    # Instalar dependencias
    if not install_dependencies():
        return
    
    # Ejecutar migraciones
    if not run_migrations():
        return
    
    # Recopilar archivos estáticos
    if not collect_static():
        return
    
    # Crear superusuario
    if not create_superuser():
        return
    
    print("\n" + "=" * 50)
    print("🎉 ¡Configuración completada exitosamente!")
    print("\n📋 Próximos pasos:")
    print("1. Ejecuta: python manage.py runserver")
    print("2. Accede a: http://localhost:8000")
    print("3. Login admin: admin / admin123")
    print("\n🌐 Para despliegue en Railway:")
    print("1. Sube tu código a GitHub")
    print("2. Conecta tu repo a Railway")
    print("3. Configura las variables de entorno")
    print("4. ¡Despliega!")

if __name__ == '__main__':
    main()
