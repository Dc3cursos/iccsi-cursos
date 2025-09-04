# 🔑 Guía para Obtener Credenciales Reales de Microsoft

## 📋 Pasos para Configurar Microsoft OAuth2

### 1. Crear Aplicación en Azure Portal

1. Ve a [Azure Portal](https://portal.azure.com/)
2. Inicia sesión con tu cuenta de Microsoft
3. Busca "Azure Active Directory" en la barra de búsqueda
4. Haz clic en **"Azure Active Directory"**

### 2. Registrar Nueva Aplicación

1. En el menú lateral, ve a **"App registrations"**
2. Haz clic en **"+ New registration"**
3. Configura la aplicación:
   - **Name**: "Instituto Capacitación IC"
   - **Supported account types**: "Accounts in any organizational directory and personal Microsoft accounts"
   - **Redirect URI**: 
     - Type: Web
     - URI: `http://127.0.0.1:8000/accounts/microsoft/login/callback/`
4. Haz clic en **"Register"**

### 3. Obtener Credenciales

1. En la página de la aplicación registrada, copia:
   - **Application (client) ID**: `12345678-1234-1234-1234-123456789012`
   - **Directory (tenant) ID**: `98765432-4321-4321-4321-210987654321`

### 4. Crear Client Secret

1. En el menú lateral, ve a **"Certificates & secrets"**
2. Haz clic en **"+ New client secret"**
3. Agrega una descripción: "Instituto Capacitación IC Secret"
4. Selecciona expiración: "24 months"
5. Haz clic en **"Add"**
6. **¡IMPORTANTE!** Copia el **Value** del secret (solo se muestra una vez)

### 5. Configurar Permisos

1. En el menú lateral, ve a **"API permissions"**
2. Haz clic en **"+ Add a permission"**
3. Selecciona **"Microsoft Graph"**
4. Selecciona **"Delegated permissions"**
5. Busca y selecciona:
   - `User.Read`
   - `email`
   - `profile`
   - `openid`
6. Haz clic en **"Add permissions"**

### 6. Actualizar en Django Admin

1. Ve a `http://127.0.0.1:8000/admin/`
2. Inicia sesión con `admin` / `admin123`
3. Ve a **Social Applications** → **Social applications**
4. Edita la aplicación "Microsoft"
5. Reemplaza:
   - **Client ID**: Con tu Application (client) ID
   - **Secret key**: Con tu Client Secret Value
6. Guarda los cambios

### 7. ¡Listo!

Ahora el botón "Continuar con Microsoft" funcionará correctamente.

## ⚠️ Notas Importantes

- **Desarrollo**: Usa `http://127.0.0.1:8000`
- **Producción**: Usa tu dominio real con HTTPS
- **Seguridad**: Nunca compartas tus credenciales
- **Client Secret**: Solo se muestra una vez, guárdalo en un lugar seguro

## 🔧 Configuración Adicional

### Para Producción:
1. Cambia el dominio en **Sites** → **Sites**
2. Actualiza las URLs de redirección en Azure Portal
3. Usa HTTPS en producción

### Troubleshooting:
- Si sigue fallando, verifica las URLs de redirección
- Asegúrate de que los permisos estén configurados
- Revisa los logs de Azure Portal

## 📞 Soporte

Si tienes problemas:
1. Verifica que la aplicación esté registrada correctamente
2. Confirma que el Client Secret no haya expirado
3. Revisa que los permisos estén habilitados
