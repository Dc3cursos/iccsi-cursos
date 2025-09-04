# ICCSI - Plataforma de Cursos Avanzados

Plataforma web para gestión de cursos de capacitación laboral con certificaciones DC-3.

## 🚀 Características

- Sistema de usuarios y autenticación
- Gestión de cursos y organizaciones
- Sistema de inscripciones
- Generación de certificados DC-3
- API REST completa
- Integración con Stripe para pagos
- Panel de administración

## 🛠️ Tecnologías

- **Backend:** Django 5.2.4
- **Base de datos:** PostgreSQL
- **API:** Django REST Framework
- **Pagos:** Stripe
- **Frontend:** Templates Django + Bootstrap

## 📋 Requisitos

- Python 3.11+
- PostgreSQL
- pip

## 🔧 Instalación

### 1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd iccsi
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
cp env.example .env
# Editar .env con tus configuraciones
```

### 5. Configurar base de datos
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear superusuario
```bash
python manage.py createsuperuser
```

### 7. Ejecutar servidor
```bash
python manage.py runserver
```

## 🌐 Acceso

- **Aplicación:** http://localhost:8000
- **Admin:** http://localhost:8000/admin/
- **API:** http://localhost:8000/api/

## 📚 Uso

1. Accede a la aplicación
2. Regístrate como usuario
3. Explora los cursos disponibles
4. Inscríbete en los cursos que te interesen
5. Completa la capacitación
6. Obtén tu certificado DC-3

## 🔐 Variables de Entorno

```env
SECRET_KEY=tu_clave_secreta
DEBUG=True
DATABASE_NAME=iccsi
DATABASE_USER=postgres
DATABASE_PASSWORD=tu_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

## 📁 Estructura del Proyecto

```
iccsi/
├── iccsi/          # Configuración principal
├── core/           # Funcionalidades core
├── usuarios/       # Gestión de usuarios
├── cursos/         # Gestión de cursos
├── media/          # Archivos subidos
├── static/         # Archivos estáticos
└── templates/      # Plantillas HTML
```

## 🚀 Despliegue

### Railway (Recomendado)
1. Conecta tu repositorio a Railway
2. Configura las variables de entorno
3. Despliega automáticamente

### Heroku
1. Instala Heroku CLI
2. Crea nueva app
3. Despliega con `git push heroku main`

## 📞 Soporte

Para soporte técnico, contacta a [tu-email@ejemplo.com]

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
