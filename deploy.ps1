# Script de Despliegue para Windows PowerShell
Write-Host "🚀 Desplegando ICCSI en Railway..." -ForegroundColor Green

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "manage.py")) {
    Write-Host "❌ Error: No se encontró manage.py. Ejecuta este script desde el directorio raíz del proyecto." -ForegroundColor Red
    exit 1
}

# Verificar configuración de seguridad
Write-Host "🔒 Verificando configuración de seguridad..." -ForegroundColor Yellow
python manage.py check --deploy

# Recopilar archivos estáticos
Write-Host "📁 Recopilando archivos estáticos..." -ForegroundColor Yellow
python manage.py collectstatic --noinput

# Hacer commit de los cambios
Write-Host "📝 Haciendo commit de los cambios..." -ForegroundColor Yellow
git add .
git commit -m "Configuración de seguridad y producción actualizada"

# Subir a GitHub
Write-Host "⬆️  Subiendo a GitHub..." -ForegroundColor Yellow
git push origin main

Write-Host "✅ ¡Despliegue completado!" -ForegroundColor Green
Write-Host "🌐 Tu aplicación estará disponible en Railway en unos minutos." -ForegroundColor Cyan
Write-Host "📱 URL: https://tu-proyecto-iccsi.railway.app" -ForegroundColor Cyan
