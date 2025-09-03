# 🔑 Guía para Obtener Credenciales Reales de Google

## 📋 Pasos para Configurar Google OAuth2

### 1. Crear Proyecto en Google Cloud Console

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Inicia sesión con tu cuenta de Google
3. Crea un nuevo proyecto o selecciona uno existente
4. Anota el **ID del proyecto**

### 2. Habilitar Google+ API

1. En el menú lateral, ve a **APIs & Services** → **Library**
2. Busca "Google+ API" o "Google Identity"
3. Haz clic en **Enable**

### 3. Crear Credenciales OAuth2

1. Ve a **APIs & Services** → **Credentials**
2. Haz clic en **+ CREATE CREDENTIALS** → **OAuth client ID**
3. Selecciona **Web application**
4. Configura:
   - **Name**: "Instituto Capacitación IC"
   - **Authorized JavaScript origins**: 
     - `http://127.0.0.1:8000` (desarrollo)
     - `https://tudominio.com` (producción)
   - **Authorized redirect URIs**:
     - `http://127.0.0.1:8000/accounts/google/login/callback/` (desarrollo)
     - `https://tudominio.com/accounts/google/login/callback/` (producción)

### 4. Obtener Credenciales

Después de crear, obtendrás:
- **Client ID**: `123456789-abcdefghijklmnop.apps.googleusercontent.com`
- **Client Secret**: `GOCSPX-abcdefghijklmnopqrstuvwxyz`

### 5. Actualizar en Django Admin

1. Ve a `http://127.0.0.1:8000/admin/`
2. Inicia sesión con `admin` / `admin123`
3. Ve a **Social Applications** → **Social applications**
4. Edita la aplicación "Google"
5. Reemplaza:
   - **Client ID**: Con tu Client ID real
   - **Secret key**: Con tu Client Secret real
6. Guarda los cambios

### 6. ¡Listo!

Ahora el botón "Continuar con Google" funcionará correctamente.

## ⚠️ Notas Importantes

- **Desarrollo**: Usa `http://127.0.0.1:8000`
- **Producción**: Usa tu dominio real con HTTPS
- **Seguridad**: Nunca compartas tus credenciales
- **Límites**: Google tiene límites de uso gratuito

## 🔧 Configuración Adicional

### Para Producción:
1. Cambia el dominio en **Sites** → **Sites**
2. Actualiza las URLs autorizadas en Google Cloud Console
3. Usa HTTPS en producción

### Troubleshooting:
- Si sigue fallando, verifica las URLs de redirección
- Asegúrate de que la API esté habilitada
- Revisa los logs de Google Cloud Console
