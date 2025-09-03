# 🚀 Guía de Despliegue en Railway

## 📋 Pasos para Desplegar tu Proyecto ICCSI

### **Paso 1: Preparar el Repositorio**

1. **Crear cuenta en GitHub** (si no tienes una)
2. **Crear un nuevo repositorio** llamado `iccsi-cursos`
3. **Subir tu código** al repositorio:

```bash
git init
git add .
git commit -m "Primer commit: Plataforma ICCSI"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/iccsi-cursos.git
git push -u origin main
```

### **Paso 2: Configurar Railway**

1. **Ir a [railway.app](https://railway.app)**
2. **Registrarse** con tu cuenta de GitHub
3. **Crear nuevo proyecto** → "Deploy from GitHub repo"
4. **Seleccionar tu repositorio** `iccsi-cursos`
5. **Esperar a que se construya** (puede tomar 5-10 minutos)

### **Paso 3: Configurar Base de Datos**

1. **En Railway, ir a "Variables"**
2. **Agregar estas variables de entorno:**

```env
SECRET_KEY=tu_clave_secreta_generada
DEBUG=False
DATABASE_NAME=railway
DATABASE_USER=postgres
DATABASE_PASSWORD=password_generado_por_railway
DATABASE_HOST=host_generado_por_railway
DATABASE_PORT=5432
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### **Paso 4: Configurar Dominio Personalizado (Opcional)**

1. **En Railway, ir a "Settings"**
2. **Sección "Domains"**
3. **Agregar tu dominio personalizado** (ej: `cursos.iccsi.com`)

### **Paso 5: Verificar Despliegue**

1. **Ir a la URL de Railway** (ej: `https://tu-proyecto.railway.app`)
2. **Verificar que la aplicación funcione**
3. **Acceder al admin:** `/admin/`

## 🔧 Solución de Problemas Comunes

### **Error: "No module named 'iccsi.iccsi'"**
- Verificar que `manage.py` esté en el directorio raíz
- Verificar la estructura de directorios

### **Error: "Database connection failed"**
- Verificar variables de entorno de base de datos
- Esperar a que Railway configure la base de datos

### **Error: "Static files not found"**
- Ejecutar `python manage.py collectstatic` localmente
- Verificar configuración de `STATIC_ROOT`

## 📱 URLs de Acceso

Una vez desplegado, tendrás acceso a:

- **Aplicación principal:** `https://tu-proyecto.railway.app`
- **Panel de admin:** `https://tu-proyecto.railway.app/admin/`
- **API REST:** `https://tu-proyecto.railway.app/api/`

## 🎯 Próximos Pasos

1. **Configurar dominio personalizado**
2. **Configurar SSL automático**
3. **Configurar backups automáticos**
4. **Configurar monitoreo**
5. **Configurar CI/CD**

## 📞 Soporte

Si tienes problemas:
1. Revisar logs en Railway
2. Verificar variables de entorno
3. Contactar soporte de Railway
4. Revisar documentación de Django

¡Tu proyecto estará funcionando en internet en menos de 30 minutos! 🎉
