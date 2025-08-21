from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File

from iccsi.cursos.models import PlantillaDC3, Organizacion, Empresa

from pathlib import Path
import unicodedata
import re


def slugify(value: str) -> str:
    value = (value or '').strip().lower()
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^a-z0-9]+', '_', value).strip('_')
    return value


class Command(BaseCommand):
    help = "Importa archivos DOCX ubicados en la carpeta 'plantillas' como PlantillaDC3 y los vincula por organizacion/empresa si es posible."

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Solo mostrar acciones sin escribir en BD')

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        roots = [
            Path(settings.BASE_DIR) / 'plantillas',
            Path(settings.BASE_DIR) / 'plantillas' / 'plantillas',  # por si el usuario guardó allí
        ]

        docx_files = []
        for root in roots:
            if root.exists():
                docx_files.extend(sorted(root.glob('dc3_*.docx')))

        if not docx_files:
            self.stdout.write(self.style.WARNING("No se encontraron archivos 'dc3_*.docx' en la carpeta 'plantillas'."))
            return

        orgs = list(Organizacion.objects.all())
        empresas = list(Empresa.objects.all())

        def find_org_or_empresa(alias: str):
            for o in orgs:
                if slugify(o.nombre) == alias:
                    return ('org', o)
            for e in empresas:
                if slugify(e.nombre) == alias:
                    return ('emp', e)
            return (None, None)

        created, updated, skipped = 0, 0, 0

        for path in docx_files:
            base = path.name  # dc3_*.docx
            stem = path.stem  # dc3_* sin extension
            suffix = stem[4:] if stem.startswith('dc3_') else stem

            target_kind, target = find_org_or_empresa(suffix)

            if base == 'dc3_plantilla.docx':
                nombre_tpl = base
                qs = PlantillaDC3.objects.filter(nombre=nombre_tpl)
                if qs.exists():
                    tpl = qs.first()
                    if not dry_run:
                        with open(path, 'rb') as f:
                            tpl.archivo.save(base, File(f), save=True)
                        tpl.organizacion = None
                        tpl.empresa = None
                        tpl.activo = True
                        tpl.save()
                    updated += 1
                    self.stdout.write(self.style.SUCCESS(f"Actualizada plantilla genérica: {base}"))
                else:
                    if not dry_run:
                        tpl = PlantillaDC3(nombre=nombre_tpl, activo=True)
                        with open(path, 'rb') as f:
                            tpl.archivo.save(base, File(f), save=True)
                        tpl.save()
                    created += 1
                    self.stdout.write(self.style.SUCCESS(f"Creada plantilla genérica: {base}"))
                continue

            if target_kind is None:
                skipped += 1
                self.stdout.write(self.style.WARNING(f"No se encontró organización/empresa para: {base}. Use ?tpl={base} para forzar o cree la organización/empresa y reintente."))
                continue

            nombre_tpl = base
            tpl_qs = PlantillaDC3.objects.filter(nombre=nombre_tpl)
            if tpl_qs.exists():
                tpl = tpl_qs.first()
                if not dry_run:
                    with open(path, 'rb') as f:
                        tpl.archivo.save(base, File(f), save=True)
                    tpl.activo = True
                    if target_kind == 'org':
                        tpl.organizacion = target
                        tpl.empresa = None
                    else:
                        tpl.empresa = target
                        tpl.organizacion = None
                    tpl.save()
                updated += 1
                self.stdout.write(self.style.SUCCESS(f"Actualizada plantilla: {base} -> {target}"))
            else:
                if not dry_run:
                    tpl = PlantillaDC3(nombre=nombre_tpl, activo=True)
                    with open(path, 'rb') as f:
                        tpl.archivo.save(base, File(f), save=True)
                    if target_kind == 'org':
                        tpl.organizacion = target
                    else:
                        tpl.empresa = target
                    tpl.save()
                created += 1
                self.stdout.write(self.style.SUCCESS(f"Creada plantilla: {base} -> {target}"))

        self.stdout.write(self.style.NOTICE(f"Resumen: creadas={created}, actualizadas={updated}, omitidas={skipped}"))



