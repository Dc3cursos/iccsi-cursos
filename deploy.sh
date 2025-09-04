#!/bin/bash

echo "🚀 Desplegando ICCSI en Railway..."

# Verificar que estamos en el directorio correcto
if [ ! -f "manage.py" ]; then
    echo "❌ Error: No se encontró manage.py. Ejecuta este script desde el directorio raíz del proyecto."
    exit 1
fi

# Verificar configuración de seguridad
echo "🔒 Verificando configuración de seguridad..."
python manage.py check --deploy

# Recopilar archivos estáticos
echo "📁 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

# Hacer commit de los cambios
echo "📝 Haciendo commit de los cambios..."
git add .
git commit -m "Configuración de seguridad y producción actualizada"

# Subir a GitHub
echo "⬆️  Subiendo a GitHub..."
git push origin main

echo "✅ ¡Despliegue completado!"
echo "🌐 Tu aplicación estará disponible en Railway en unos minutos."
echo "📱 URL: https://tu-proyecto-iccsi.railway.app"
