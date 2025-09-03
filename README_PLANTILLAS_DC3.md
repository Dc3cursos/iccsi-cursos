# 📋 Sistema de Plantillas DC-3 - ICCSI

## 🎯 Descripción

Este sistema permite llenar plantillas de certificados DC-3 directamente en el navegador, con firmas electrónicas integradas, sin necesidad de generar archivos externos. Las plantillas con firmas se mantienen seguras dentro del sistema.

## ✨ Características Principales

- **🖥️ Llenado en el Sistema**: Las plantillas se llenan directamente en el navegador
- **✍️ Firmas Electrónicas**: Sistema de firma digital integrado con canvas
- **👁️ Previsualización**: Vista previa en tiempo real antes de generar el PDF
- **🎨 Múltiples Plantillas**: Soporte para diferentes plantillas por organización
- **📱 Responsive**: Funciona en dispositivos móviles y de escritorio
- **🔒 Seguridad**: Las firmas se mantienen dentro del sistema

## 🚀 Instalación y Configuración

### 1. Ejecutar Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Cargar Plantillas Existentes

```bash
python cargar_plantillas.py
```

Este script:
- Busca plantillas PDF en `media/plantillas/dc3/`
- Las registra automáticamente en la base de datos
- Crea plantillas de ejemplo si no encuentra ninguna

### 3. Crear Superusuario (si no existe)

```bash
python manage.py createsuperuser
```

### 4. Ejecutar el Servidor

```bash
python manage.py runserver
```

## 📖 Uso del Sistema

### Acceso al Sistema

1. Inicia sesión en el sistema
2. Ve al menú "📋 Certificados DC-3"
3. O accede directamente a: `http://localhost:8000/cursos/dc3/llenar-plantilla-sistema/`

### Proceso de Generación de Certificados

#### Paso 1: Seleccionar Plantilla
- Elige una de las plantillas disponibles
- Cada plantilla puede estar asociada a una organización específica

#### Paso 2: Llenar Información
- **Información del Trabajador**: Datos personales y laborales
- **Información del Curso**: Detalles del curso de capacitación
- **Información de la Empresa**: Datos de la empresa contratante
- **Fechas del Curso**: Período de capacitación
- **Información del Instructor**: Datos del instructor

#### Paso 3: Firma Electrónica
- Dibuja tu firma en el área de firma
- Usa el botón "Limpiar Firma" si necesitas rehacerla
- La firma se guarda automáticamente

#### Paso 4: Previsualizar
- Haz clic en "👁️ Previsualizar" para ver el certificado
- Revisa que toda la información sea correcta
- Puedes imprimir la vista previa

#### Paso 5: Generar PDF Final
- Haz clic en "📄 Generar Certificado"
- El sistema genera un PDF con la firma integrada
- El archivo se descarga automáticamente

## 🛠️ Administración de Plantillas

### Acceso al Admin

1. Ve a `http://localhost:8000/admin/`
2. Inicia sesión con tu superusuario
3. Busca la sección "Plantillas DC-3"

### Gestión de Plantillas

#### Crear Nueva Plantilla

1. En el admin, ve a "Plantillas DC-3" → "Añadir plantilla DC-3"
2. Completa los campos:
   - **Nombre**: Nombre descriptivo de la plantilla
   - **Archivo**: Sube el archivo PDF de la plantilla
   - **Organización**: Asocia con una organización (opcional)
   - **Empresa**: Asocia con una empresa específica (opcional)
   - **Activo**: Marca si la plantilla está disponible

#### Editar Plantillas Existentes

- Cambia el estado activo/inactivo
- Actualiza el archivo de la plantilla
- Modifica la organización asociada

### Gestión de Logos

El sistema también permite gestionar logos para las plantillas:

1. Ve a "Logos DC-3" en el admin
2. Sube imágenes de logos
3. Asócialos con organizaciones o empresas específicas

## 📁 Estructura de Archivos

```
media/
├── plantillas/
│   ├── dc3/                    # Plantillas PDF
│   │   ├── CERTIFICADO_DC-3_FRATERNIDAD_MIGRATORIA.pdf
│   │   └── CERTIFICADO_DC3_cpi.pdf
│   └── logos/                  # Logos de organizaciones
│       ├── logo_iccsi.png
│       └── logo_fraternidad.png
```

## 🔧 Personalización

### Modificar Estilos

Los estilos están en los templates:
- `iccsi/cursos/templates/cursos/llenar_plantilla_sistema.html`
- `iccsi/cursos/templates/cursos/previsualizar_certificado.html`

### Agregar Nuevos Campos

1. Modifica el modelo `DC3GenerateForm` en `forms.py`
2. Actualiza las vistas en `views.py`
3. Modifica los templates HTML

### Cambiar Plantillas PDF

1. Sube la nueva plantilla al admin
2. O reemplaza el archivo en `media/plantillas/dc3/`
3. Ejecuta `python cargar_plantillas.py` para actualizar

## 🐛 Solución de Problemas

### Error: "No hay plantillas disponibles"

1. Ejecuta `python cargar_plantillas.py`
2. Verifica que existan archivos PDF en `media/plantillas/dc3/`
3. Crea plantillas manualmente desde el admin

### Error: "Plantilla no encontrada"

1. Verifica que la plantilla esté marcada como "Activa"
2. Revisa que el archivo PDF esté subido correctamente
3. Ejecuta `python manage.py collectstatic` si es necesario

### Problemas con Firmas

1. Asegúrate de que el navegador soporte Canvas
2. Prueba en un navegador diferente
3. Verifica que JavaScript esté habilitado

## 📞 Soporte

Para problemas técnicos o preguntas:

1. Revisa los logs del servidor Django
2. Verifica la consola del navegador para errores JavaScript
3. Consulta la documentación de Django

## 🔄 Actualizaciones

Para actualizar el sistema:

1. Haz backup de la base de datos
2. Actualiza el código
3. Ejecuta las migraciones: `python manage.py migrate`
4. Reinicia el servidor

## 📋 Checklist de Implementación

- [ ] Migraciones ejecutadas
- [ ] Plantillas cargadas con `cargar_plantillas.py`
- [ ] Superusuario creado
- [ ] Archivos de plantillas en `media/plantillas/dc3/`
- [ ] Servidor ejecutándose
- [ ] Acceso al sistema funcionando
- [ ] Generación de certificados probada
- [ ] Firmas electrónicas funcionando

## 🎉 ¡Listo!

Tu sistema de plantillas DC-3 está listo para usar. Los usuarios pueden ahora generar certificados directamente en el sistema con firmas integradas, manteniendo la seguridad de las plantillas originales.
