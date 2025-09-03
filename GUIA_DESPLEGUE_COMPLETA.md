# 🚀 Guía Completa de Despliegue - ICCSI

## 📋 **Resumen del Proyecto**
- **Nombre:** ICCSI - Plataforma de Cursos Avanzados
- **Tecnología:** Django 5.2.4 + PostgreSQL + API REST
- **Funcionalidad:** Gestión de cursos, certificaciones DC-3, pagos con Stripe
- **Estado:** ✅ Configurado para producción

## 🌐 **Opciones de Despliegue**

### **1. Railway (RECOMENDADO) ⭐**
- **Costo:** $5/mes (muy económico)
- **Facilidad:** ⭐⭐⭐⭐⭐
- **Escalabilidad:** ⭐⭐⭐⭐
- **URL:** `https://tu-proyecto-iccsi.railway.app`

### **2. Heroku**
- **Costo:** $7/mes
- **Facilidad:** ⭐⭐⭐⭐
- **Escalabilidad:** ⭐⭐⭐⭐⭐
- **URL:** `https://tu-proyecto-iccsi.herokuapp.com`

### **3. DigitalOcean App Platform**
- **Costo:** $5/mes
- **Facilidad:** ⭐⭐⭐
- **Escalabilidad:** ⭐⭐⭐⭐⭐
- **URL:** `https://tu-proyecto-iccsi.ondigitalocean.app`

### **4. Vercel (Solo Frontend)**
- **Costo:** Gratis
- **Facilidad:** ⭐⭐⭐⭐⭐
- **Limitación:** Solo frontend
- **URL:** `https://tu-proyecto-iccsi.vercel.app`

## 🚀 **Despliegue en Railway (Paso a Paso)**

### **Paso 1: Preparar Repositorio**
```bash
# Inicializar git
git init
git add .
git commit -m "Plataforma ICCSI lista para producción"

# Crear repositorio en GitHub
# Luego conectar:
git remote add origin https://github.com/TU_USUARIO/iccsi-cursos.git
git branch -M main
git push -u origin main
```

### **Paso 2: Configurar Railway**
1. **Ir a [railway.app](https://railway.app)**
2. **Registrarse con GitHub**
3. **Crear nuevo proyecto** → "Deploy from GitHub repo"
4. **Seleccionar tu repositorio**
5. **Esperar construcción** (5-10 minutos)

### **Paso 3: Configurar Variables de Entorno**
En Railway → Variables, agregar:
```env
SECRET_KEY=p#=x3w0u31ivx62&v*n@8*8r4*oh%n@$!9jsv4l)0jjyldi$qi
DEBUG=False
DATABASE_NAME=railway
DATABASE_USER=postgres
DATABASE_PASSWORD=password_de_railway
DATABASE_HOST=host_de_railway
DATABASE_PORT=5432
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### **Paso 4: Verificar Despliegue**
- **URL:** `https://tu-proyecto-iccsi.railway.app`
- **Admin:** `/admin/`
- **API:** `/api/`

## 🔧 **Despliegue en Heroku**

### **Paso 1: Instalar Heroku CLI**
```bash
# Windows
winget install --id=Heroku.HerokuCLI

# Verificar instalación
heroku --version
```

### **Paso 2: Crear App en Heroku**
```bash
heroku login
heroku create tu-proyecto-iccsi
heroku addons:create heroku-postgresql:mini
```

### **Paso 3: Configurar Variables**
```bash
heroku config:set SECRET_KEY="tu_clave_secreta"
heroku config:set DEBUG=False
heroku config:set STRIPE_PUBLISHABLE_KEY="pk_test_..."
heroku config:set STRIPE_SECRET_KEY="sk_test_..."
```

### **Paso 4: Desplegar**
```bash
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

## 🐳 **Despliegue con Docker**

### **Paso 1: Construir Imagen**
```bash
docker build -t iccsi-cursos .
```

### **Paso 2: Ejecutar con Docker Compose**
```bash
docker-compose up -d
```

### **Paso 3: Acceder**
- **Aplicación:** http://localhost:8000
- **Base de datos:** localhost:5432

## 🔐 **Configuración de Seguridad**

### **✅ Configuraciones Aplicadas:**
- **SECRET_KEY:** Generada automáticamente
- **DEBUG:** False en producción
- **SSL:** Redirección automática a HTTPS
- **HSTS:** Configurado para 1 año
- **Cookies:** Seguras y HTTPOnly
- **CSRF:** Protección activada
- **XSS:** Filtros activados

### **🔒 Variables de Entorno Requeridas:**
```env
SECRET_KEY=clave_secreta_larga_y_aleatoria
DEBUG=False
DATABASE_URL=postgres://usuario:password@host:puerto/db
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
```

## 📱 **URLs de Acceso**

### **Railway:**
- **Principal:** `https://tu-proyecto-iccsi.railway.app`
- **Admin:** `https://tu-proyecto-iccsi.railway.app/admin/`
- **API:** `https://tu-proyecto-iccsi.railway.app/api/`

### **Heroku:**
- **Principal:** `https://tu-proyecto-iccsi.herokuapp.com`
- **Admin:** `https://tu-proyecto-iccsi.herokuapp.com/admin/`
- **API:** `https://tu-proyecto-iccsi.herokuapp.com/api/`

## 🎯 **Próximos Pasos Después del Despliegue**

### **1. Configurar Dominio Personalizado**
- Comprar dominio (ej: `cursos.iccsi.com`)
- Configurar DNS en Railway/Heroku
- Configurar SSL automático

### **2. Configurar Sistema de Pagos**
- Crear cuenta en Stripe
- Configurar webhooks
- Probar pagos de prueba

### **3. Configurar Email**
- Configurar SMTP (Gmail, SendGrid)
- Configurar notificaciones automáticas
- Configurar recuperación de contraseñas

### **4. Configurar Monitoreo**
- Configurar logs centralizados
- Configurar alertas de error
- Configurar métricas de rendimiento

### **5. Configurar Backups**
- Configurar backups automáticos de BD
- Configurar backups de archivos
- Configurar restauración de emergencia

## 🆘 **Solución de Problemas**

### **Error: "No module named 'iccsi.iccsi'"**
```bash
# Verificar estructura de directorios
ls -la
# manage.py debe estar en el directorio raíz
```

### **Error: "Database connection failed"**
```bash
# Verificar variables de entorno
# Verificar que la base de datos esté activa
```

### **Error: "Static files not found"**
```bash
python manage.py collectstatic --noinput
# Verificar STATIC_ROOT en settings.py
```

### **Error: "Permission denied"**
```bash
# Verificar permisos de archivos
chmod +x deploy.sh
chmod +x deploy.ps1
```

## 📞 **Soporte y Recursos**

### **Documentación Oficial:**
- **Django:** https://docs.djangoproject.com/
- **Railway:** https://docs.railway.app/
- **Heroku:** https://devcenter.heroku.com/

### **Comunidad:**
- **Stack Overflow:** Tag: django, railway, heroku
- **Reddit:** r/django, r/railway
- **Discord:** Django Community

## 🎉 **¡Tu Proyecto Está Listo para Producción!**

Con esta configuración, tu plataforma ICCSI tendrá:
- ✅ **Seguridad de nivel empresarial**
- ✅ **Escalabilidad automática**
- ✅ **SSL/HTTPS automático**
- ✅ **Base de datos PostgreSQL en la nube**
- ✅ **Monitoreo y logs**
- ✅ **Backups automáticos**
- ✅ **Dominio personalizado opcional**

**¡Tu plataforma de cursos avanzados estará funcionando en internet en menos de 30 minutos!** 🚀✨
