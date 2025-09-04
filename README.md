# ICCSI Cursos

Plataforma abierta para la gestión de cursos, profesores y certificados DC-3 profesional.

## Características

- Gestión completa de cursos, profesores y alumnos.
- Generación y protección de certificados DC-3.
- Sistema de pagos: Stripe, PayPal, MercadoPago.
- Facturación profesional.
- Verificación de autenticidad de certificados.
- Paneles de administración y usuario.
- Despliegue multiplataforma (Web, Escritorio, Móvil, API REST).
- Seguridad y autenticación social.

## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/Dc3cursos/iccsi-cursos.git
    cd iccsi-cursos
    ```
2. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
3. Copia el archivo de entorno y configúralo:
    ```bash
    cp .env.example .env
    # Edita .env con tus variables reales
    ```

## Despliegue rápido (Docker)

```bash
docker build -t iccsi-cursos .
docker-compose up -d
```

Consulta la documentación en los archivos `.md` para despliegues Railway, Heroku y autenticación social.

## Contribuir

- Haz un fork del repositorio.
- Crea tu rama: `git checkout -b feature/nueva-funcionalidad`
- Haz tus cambios y crea un pull request.
- ¡Tus sugerencias y mejoras son bienvenidas!

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más información.