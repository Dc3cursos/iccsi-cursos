import json
import unicodedata
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from iccsi.usuarios.models import Usuario
from iccsi.cursos.models import Curso, Organizacion

DEFAULT_IMAGE_REL_PATH = "cursos/imagenes/default.png"


def ensure_default_image_exists(media_root: Path) -> Path | None:
    """Crea una imagen placeholder si no existe. Devuelve la ruta al archivo o None si falla."""
    default_path = media_root / DEFAULT_IMAGE_REL_PATH
    if default_path.exists():
        return default_path
    default_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        from PIL import Image, ImageDraw, ImageFont

        width, height = 960, 540
        img = Image.new("RGB", (width, height), color=(238, 242, 248))
        draw = ImageDraw.Draw(img)
        text = "Curso"
        # Intentar una fuente común; si falla, usar la por defecto
        try:
            font = ImageFont.truetype("arial.ttf", 64)
        except Exception:
            font = ImageFont.load_default()
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        draw.text(
            ((width - text_width) / 2, (height - text_height) / 2),
            text,
            font=font,
            fill=(45, 55, 72),
        )
        img.save(default_path)
        return default_path
    except Exception:
        # Si no está Pillow o algo falla, no forzar error
        return None


def normalize_whitespace(text: str) -> str:
    if not text:
        return ""
    text = unicodedata.normalize("NFKC", text)
    # Colapsar espacios múltiples
    return " ".join(text.split())


def generar_descripcion(nombre: str, horas: int, organizacion: str) -> str:
    nombre_limpio = normalize_whitespace(nombre)
    partes = nombre_limpio.split(",")
    tema_base = partes[0].strip() if partes else nombre_limpio
    return (
        f"Capacitación en {tema_base.lower().capitalize()}. "
        f"Duración estimada: {horas} horas. "
        f"Emitido por {organizacion}."
    )


class Command(BaseCommand):
    help = "Importa cursos desde cursos_por_organizacion.json creando Cursos con horas y una descripción breve"

    def add_arguments(self, parser):
        parser.add_argument(
            "--profesor",
            dest="profesor_username",
            help="Username del profesor propietario de los cursos (opcional). Si no se indica, toma el primer usuario con rol 'profesor' o el primer superusuario.",
        )

    def handle(self, *args, **options):
        ruta_json = Path(settings.BASE_DIR) / "cursos_por_organizacion.json"
        if not ruta_json.exists():
            raise CommandError(f"No se encontró {ruta_json}")

        try:
            data = json.loads(ruta_json.read_text(encoding="utf-8"))
        except Exception as exc:
            raise CommandError(f"No se pudo leer el JSON: {exc}")

        profesor = None
        username = options.get("profesor_username")
        if username:
            profesor = Usuario.objects.filter(username=username).first()
            if not profesor:
                raise CommandError(f"No existe usuario profesor con username='{username}'")
        if not profesor:
            profesor = Usuario.objects.filter(rol="profesor").first() or Usuario.objects.filter(is_superuser=True).first()
        if not profesor:
            raise CommandError("No hay profesor ni superusuario disponible para asignar como propietario de los cursos")

        creados = 0
        actualizados = 0

        # Garantizar placeholder de imagen
        default_image_file = ensure_default_image_exists(Path(settings.MEDIA_ROOT))

        for nombre_org, cursos in (data or {}).items():
            if not isinstance(cursos, list):
                continue
            org_obj, _ = Organizacion.objects.get_or_create(nombre=nombre_org)
            for item in cursos:
                nombre = normalize_whitespace(str(item.get("curso", "")).strip())
                horas = item.get("horas")
                if not nombre or not isinstance(horas, int):
                    continue
                descripcion = generar_descripcion(nombre, horas, nombre_org)

                defaults = {
                    "descripcion": descripcion,
                    "duracion_horas": horas,
                    "profesor": profesor,
                    "organizacion": org_obj,
                }
                if default_image_file:
                    defaults["imagen"] = DEFAULT_IMAGE_REL_PATH

                # Identificar por (nombre, organizacion) para no mezclar entre organizaciones
                curso, created = Curso.objects.get_or_create(
                    nombre=nombre,
                    organizacion=org_obj,
                    defaults=defaults,
                )
                if created:
                    creados += 1
                else:
                    # Actualiza datos clave si cambiaron
                    cambios = False
                    if curso.duracion_horas != horas:
                        curso.duracion_horas = horas
                        cambios = True
                    if not curso.descripcion:
                        curso.descripcion = descripcion
                        cambios = True
                    if curso.organizacion_id != org_obj.id:
                        curso.organizacion = org_obj
                        cambios = True
                    if default_image_file and not curso.imagen:
                        # asignar placeholder si no tiene
                        curso.imagen.name = DEFAULT_IMAGE_REL_PATH
                        cambios = True
                    if cambios:
                        # Guardar solo campos cambiados; 'imagen' se incluye si fue asignada
                        campos = ["duracion_horas", "descripcion", "organizacion"]
                        if curso.imagen:
                            campos.append("imagen")
                        curso.save(update_fields=campos)
                        actualizados += 1

        self.stdout.write(self.style.SUCCESS(
            f"Importación finalizada. Cursos creados: {creados}. Cursos actualizados: {actualizados}."
        ))


