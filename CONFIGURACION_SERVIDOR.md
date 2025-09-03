# 🚀 CONFIGURACIÓN DEL SERVIDOR DJANGO

## 📋 Información del Sistema

- **Framework**: Django 5.2.4
- **URL del servidor**: `http://127.0.0.1:8000`
- **Puerto**: 8000
- **Sistema Operativo**: Windows 10/11

## 🔧 Métodos para Iniciar el Servidor

### Método 1: Comando Directo (Recomendado)
```powershell
python manage.py runserver 127.0.0.1:8000
```

### Método 2: Proceso en Segundo Plano (Windows)
```powershell
Start-Process python -ArgumentList "manage.py", "runserver", "127.0.0.1:8000" -WindowStyle Hidden
```

### Método 3: Script Batch
```batch
iniciar_servidor.bat
```

## 🔍 Verificar Estado del Servidor

### Verificar si el puerto está en uso:
```powershell
netstat -an | findstr :8000
```

### Probar respuesta del servidor:
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000" -UseBasicParsing | Select-Object StatusCode
```

## 👤 Credenciales de Acceso

### Profesor Eduardo Mendieta:
- **Usuario**: `eduardo_mendieta_zuñiga`
- **Contraseña**: `password123`
- **Rol**: Profesor
- **Panel**: `http://127.0.0.1:8000/usuarios/panel/profesor/`

## 📚 Recursos del Sistema

### URLs Principales:
- **Página principal**: `http://127.0.0.1:8000`
- **Dashboard**: `http://127.0.0.1:8000/dashboard/`
- **Panel del profesor**: `http://127.0.0.1:8000/usuarios/panel/profesor/`
- **Lista de cursos**: `http://127.0.0.1:8000/cursos/`
- **Crear curso**: `http://127.0.0.1:8000/cursos/crear/`
- **Certificados**: `http://127.0.0.1:8000/cursos/llenar-pdf/`

### Base de Datos:
- **Total de cursos**: 269 cursos
- **Organizaciones**: 2 organizaciones
- **Profesor**: Eduardo Mendieta Zuñiga

## 🛠️ Solución de Problemas

### Si el servidor no inicia:
1. Verificar que Python esté instalado
2. Verificar que Django esté instalado: `pip install django`
3. Verificar que estés en el directorio correcto
4. Verificar que no haya otro proceso usando el puerto 8000

### Si el servidor se detiene:
1. Usar el método de proceso en segundo plano
2. Verificar logs de error
3. Reiniciar el servidor

## 📝 Notas Importantes

- El servidor está configurado para desarrollo local
- Los archivos de media se guardan en `iccsi/media/`
- La base de datos es SQLite por defecto
- El modo DEBUG está activado para desarrollo

---
**Última actualización**: Hoy
**Estado**: ✅ OPERATIVO
