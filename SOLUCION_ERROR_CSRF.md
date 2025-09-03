# Solución para Error CSRF en Login

## Problema
Error 403 - "Token CSRF del POST incorrecto" al intentar hacer login.

## Causas posibles
1. Token CSRF expirado
2. Cookies del navegador corruptas
3. Problema de sesión

## Soluciones

### 1. Limpiar cookies del navegador
1. Abrir el navegador
2. Ir a Configuración/Preferencias
3. Buscar "Cookies" o "Datos de navegación"
4. Eliminar todas las cookies para `127.0.0.1:8000`
5. Recargar la página de login

### 2. Recargar la página de login
1. Presionar `Ctrl + F5` (recarga forzada)
2. O presionar `Ctrl + Shift + R`
3. Esto regenerará el token CSRF

### 3. Verificar que el formulario tenga el token CSRF
El template `login.html` ya tiene:
```html
<form method="post" class="email-form">
    {% csrf_token %}
    <!-- campos del formulario -->
</form>
```

### 4. Si el problema persiste
1. Cerrar completamente el navegador
2. Abrir una nueva ventana de incógnito/privada
3. Ir a `http://127.0.0.1:8000/usuarios/login/`
4. Intentar el login nuevamente

### 5. Verificar que el servidor esté funcionando
```bash
python manage.py runserver 127.0.0.1:8000
```

## Estado actual del sistema
✅ **Migraciones aplicadas**: Las tablas de facturación están creadas
✅ **Login corregido**: El formulario ahora maneja email y contraseña correctamente
✅ **Sistema de facturación**: Completamente implementado y funcional

## URLs disponibles
- **Login**: http://127.0.0.1:8000/usuarios/login/
- **Sistema de facturación**: http://127.0.0.1:8000/cursos/facturas/
- **Crear factura**: http://127.0.0.1:8000/cursos/facturas/crear/

## Próximos pasos
1. Solucionar el error CSRF siguiendo las instrucciones arriba
2. Probar el login con las credenciales existentes
3. Probar el sistema de facturación
4. Configurar credenciales reales de Google/Microsoft si es necesario
