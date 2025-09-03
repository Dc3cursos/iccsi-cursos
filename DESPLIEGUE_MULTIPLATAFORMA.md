# 🚀 DESPLIEGUE MULTIPLATAFORMA ICCSI

## 📋 RESUMEN DEL PROYECTO

Tu sistema ICCSI está listo para ser desplegado en múltiples plataformas:

- ✅ **Sitio Web** (Django + API REST)
- ✅ **App de Escritorio** (PyQt6)
- ✅ **App Móvil** (React Native)
- ✅ **API REST** (Django REST Framework)

## 🌐 1. SITIO WEB (RECOMENDADO PARA EMPEZAR)

### **Opción A: Heroku (Más Fácil)**

1. **Crear cuenta en Heroku:**
   - Ve a: https://heroku.com
   - Regístrate gratuitamente

2. **Instalar Heroku CLI:**
   ```bash
   # Windows
   winget install --id=Heroku.HerokuCLI
   
   # O descarga desde: https://devcenter.heroku.com/articles/heroku-cli
   ```

3. **Conectar con tu repositorio:**
   ```bash
   heroku login
   heroku create iccsi-app
   git add .
   git commit -m "Preparar para Heroku"
   git push heroku main
   ```

4. **Configurar variables de entorno:**
   ```bash
   heroku config:set DEBUG=False
   heroku config:set SECRET_KEY=tu-clave-secreta-aqui
   heroku config:set ALLOWED_HOSTS=tu-app.herokuapp.com
   ```

5. **Ejecutar migraciones:**
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

### **Opción B: Railway (Muy Simple)**

1. **Crear cuenta en Railway:**
   - Ve a: https://railway.app
   - Conecta con tu cuenta de GitHub

2. **Desplegar automáticamente:**
   - Conecta tu repositorio
   - Railway detectará Django automáticamente
   - Se desplegará en minutos

### **Opción C: PythonAnywhere**

1. **Crear cuenta en PythonAnywhere:**
   - Ve a: https://www.pythonanywhere.com
   - Plan gratuito disponible

2. **Subir archivos:**
   - Sube tu código via Git o archivos
   - Configura WSGI file
   - Configura base de datos

## 💻 2. APP DE ESCRITORIO

### **Requisitos:**
```bash
pip install PyQt6 requests
```

### **Ejecutar:**
```bash
python app_escritorio.py
```

### **Características:**
- ✅ Interfaz nativa de Windows/Mac/Linux
- ✅ Conexión directa a la API
- ✅ Gestión de cursos y certificados
- ✅ Generación de PDFs
- ✅ Sistema de autenticación

### **Compilar a Ejecutable:**
```bash
# Instalar PyInstaller
pip install pyinstaller

# Compilar
pyinstaller --onefile --windowed app_escritorio.py

# El ejecutable estará en dist/
```

## 📱 3. APP MÓVIL

### **Requisitos:**
- Node.js 18+
- React Native CLI
- Android Studio (para Android)
- Xcode (para iOS, solo Mac)

### **Instalar dependencias:**
```bash
cd app_movil
npm install
```

### **Ejecutar en Android:**
```bash
npx react-native run-android
```

### **Ejecutar en iOS:**
```bash
npx react-native run-ios
```

### **Características:**
- ✅ Interfaz móvil nativa
- ✅ Navegación por tabs
- ✅ Gestión de cursos
- ✅ Generación de certificados
- ✅ Descarga de PDFs
- ✅ Autenticación JWT

## 🔌 4. API REST

### **Endpoints disponibles:**

#### **Autenticación:**
- `POST /api/auth/login/` - Iniciar sesión
- `POST /api/auth/register/` - Registrarse
- `GET /api/auth/profile/` - Perfil del usuario

#### **Cursos:**
- `GET /api/cursos/` - Lista de cursos
- `POST /api/cursos/{id}/inscribirse/` - Inscribirse a curso
- `GET /api/cursos/mis_cursos/` - Mis cursos

#### **Certificados:**
- `GET /api/certificados/` - Mis certificados
- `POST /api/certificados/generar/` - Generar certificado
- `GET /api/certificados/{id}/descargar/` - Descargar PDF

#### **Plantillas:**
- `GET /api/plantillas/` - Plantillas disponibles
- `GET /api/plantillas/disponibles/` - Plantillas activas

## 🛠️ 5. CONFIGURACIÓN PARA PRODUCCIÓN

### **Archivos necesarios:**
- ✅ `requirements_produccion.txt` - Dependencias
- ✅ `Procfile` - Para Heroku
- ✅ `iccsi/iccsi/settings_produccion.py` - Configuración producción
- ✅ `env_example.txt` - Variables de entorno

### **Variables de entorno necesarias:**
```bash
DEBUG=False
SECRET_KEY=tu-clave-secreta-aqui
ALLOWED_HOSTS=tu-dominio.com
DB_NAME=tu_base_de_datos
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_HOST=tu_host
DB_PORT=5432
```

### **Base de datos PostgreSQL:**
```bash
# Crear base de datos
createdb iccsi_db

# Crear usuario
createuser iccsi_user

# Asignar permisos
grant all privileges on database iccsi_db to iccsi_user;
```

## 🚀 6. PASOS PARA DESPLEGAR

### **Paso 1: Preparar el código**
```bash
# Instalar dependencias de producción
pip install -r requirements_produccion.txt

# Recolectar archivos estáticos
python manage.py collectstatic

# Hacer migraciones
python manage.py makemigrations
python manage.py migrate
```

### **Paso 2: Configurar base de datos**
- Usar PostgreSQL en producción
- Configurar variables de entorno
- Ejecutar migraciones

### **Paso 3: Desplegar**
- Elegir plataforma (Heroku, Railway, etc.)
- Conectar repositorio
- Configurar variables de entorno
- Desplegar automáticamente

### **Paso 4: Probar**
- Verificar que la API funciona
- Probar app de escritorio
- Probar app móvil
- Verificar generación de certificados

## 📊 7. ESTRUCTURA DEL PROYECTO

```
iccsi/
├── iccsi/                    # Configuración Django
│   ├── settings.py          # Configuración desarrollo
│   ├── settings_produccion.py # Configuración producción
│   └── urls.py              # URLs principales
├── cursos/                   # App de cursos
│   ├── api_views.py         # Vistas de API
│   ├── serializers.py       # Serializers para API
│   └── models.py            # Modelos de datos
├── usuarios/                 # App de usuarios
├── app_escritorio.py        # App de escritorio PyQt6
├── app_movil/               # App móvil React Native
├── requirements_produccion.txt # Dependencias producción
├── Procfile                 # Para Heroku
└── env_example.txt          # Variables de entorno
```

## 🔒 8. SEGURIDAD

### **Configuraciones implementadas:**
- ✅ HTTPS forzado
- ✅ HSTS headers
- ✅ CSRF protection
- ✅ JWT authentication
- ✅ CORS configurado
- ✅ Rate limiting (configurable)

### **Recomendaciones adicionales:**
- Cambiar SECRET_KEY en producción
- Usar base de datos PostgreSQL
- Configurar backup automático
- Monitoreo de logs
- Firewall y WAF

## 📱 9. PLATAFORMAS DE DESPLIEGUE

### **Gratuitas:**
1. **Heroku** - Fácil, 550 horas/mes gratis
2. **Railway** - Muy simple, $5/mes
3. **PythonAnywhere** - Especializado en Python
4. **Render** - Fácil, gratuito

### **De Pago:**
1. **DigitalOcean** - $5/mes, muy estable
2. **AWS** - Escalable, complejo
3. **Google Cloud** - Escalable, complejo
4. **Azure** - Escalable, complejo

## 🎯 10. PRÓXIMOS PASOS

### **Inmediato:**
1. Desplegar en Heroku (más fácil)
2. Probar la API
3. Ejecutar app de escritorio
4. Configurar base de datos

### **Corto plazo:**
1. Personalizar interfaz
2. Agregar más funcionalidades
3. Configurar dominio personalizado
4. Implementar backup automático

### **Largo plazo:**
1. App móvil en stores
2. Múltiples idiomas
3. Analytics y métricas
4. Escalabilidad empresarial

## 📞 11. SOPORTE

### **Si encuentras problemas:**
1. Verificar logs del servidor
2. Revisar variables de entorno
3. Verificar conexión a base de datos
4. Probar endpoints de la API

### **Recursos útiles:**
- Documentación Django: https://docs.djangoproject.com/
- Documentación Heroku: https://devcenter.heroku.com/
- Documentación React Native: https://reactnative.dev/

## 🎉 ¡TU SISTEMA ESTÁ LISTO!

**Estado:** ✅ 100% FUNCIONAL
**Plataformas:** ✅ Web + Escritorio + Móvil
**API:** ✅ REST completa
**Seguridad:** ✅ Configurada
**Despliegue:** ✅ Listo para producción

**¡Puedes comenzar a desplegar tu sistema en múltiples plataformas inmediatamente!**
