from django.contrib import admin
from .models import Curso, Inscripcion, Organizacion, Recurso, PlantillaDC3, LogoDC3, HistorialCertificadoDC3
from django.http import HttpResponse
from django.conf import settings
import os
from tempfile import TemporaryDirectory

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = (
        'miniatura',
        'nombre',
        'organizacion',
        'duracion_horas',
        'profesor',
        'fecha_creacion',
        'num_inscritos',
    )
    search_fields = ('nombre', 'profesor__username', 'organizacion__nombre')
    list_filter = ('profesor', 'fecha_creacion', 'organizacion')

    def num_inscritos(self, obj):
        return obj.inscripciones.count()
    num_inscritos.short_description = 'Alumnos Inscritos'

    def miniatura(self, obj):
        if obj.imagen:
            return f"<img src='{obj.imagen.url}' style='height:40px;width:72px;object-fit:cover;border-radius:4px' />"
        return ""
    miniatura.short_description = 'Imagen'
    miniatura.allow_tags = True


@admin.register(Organizacion)
class OrganizacionAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(Recurso)
class RecursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'curso')
    search_fields = ('nombre', 'curso__nombre')
    list_filter = ('curso',)

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'alumno_email', 'curso', 'fecha_inscripcion')
    search_fields = ('alumno__username', 'alumno__email', 'curso__nombre')
    list_filter = ('curso', 'alumno', 'fecha_inscripcion')

    def alumno_email(self, obj):
        return obj.alumno.email
    alumno_email.short_description = 'Email Alumno'


@admin.register(PlantillaDC3)
class PlantillaDC3Admin(admin.ModelAdmin):
    list_display = ('nombre', 'organizacion', 'empresa', 'activo', 'creado')
    list_filter = ('activo', 'organizacion', 'empresa')
    search_fields = ('nombre', 'organizacion__nombre', 'empresa__nombre')
    actions = ['vista_previa_docx', 'vista_previa_pdf']

    def _build_context(self, obj: PlantillaDC3):
        from datetime import date, timedelta
        inicio = date.today()
        fin = inicio + timedelta(days=1)

        # Buscar logo asociado
        logo_obj = None
        if obj.organizacion:
            logo_obj = LogoDC3.objects.filter(organizacion=obj.organizacion, activo=True).first()
        if not logo_obj and obj.empresa:
            logo_obj = LogoDC3.objects.filter(empresa=obj.empresa, activo=True).first()
        if not logo_obj:
            logo_obj = LogoDC3.objects.filter(organizacion__isnull=True, empresa__isnull=True, activo=True).first()

        ctx = {
            'APELLIDO_PATERNO': 'PATERNO',
            'APELLIDO_MATERNO': 'MATERNO',
            'NOMBRES': 'NOMBRES',
            'CURP': 'CURPXXXXYYYYZZZZ11',
            'OCUPACION': 'Ocupación de ejemplo',
            'PUESTO': 'Puesto de ejemplo',
            'RAZON_SOCIAL': obj.empresa.nombre if obj.empresa else (obj.organizacion.nombre if obj.organizacion else 'Empresa/Org genérica'),
            'RFC': 'RFC123456ABC',
            'NOMBRE_CURSO': 'Curso de ejemplo',
            'HORAS': 8,
            'DIA_INICIO': f"{inicio.day:02d}",
            'MES_INICIO': f"{inicio.month:02d}",
            'ANIO_INICIO': f"{inicio.year}",
            'DIA_FIN': f"{fin.day:02d}",
            'MES_FIN': f"{fin.month:02d}",
            'ANIO_FIN': f"{fin.year}",
            'AREA_TEMATICA': '—',
            'AGENTE_CAPACITADOR': obj.organizacion.nombre if obj.organizacion else '—',
            'REGISTRO_AGENTE': '—',
            'INSTRUCTOR_NOMBRE': 'EDUARDO MENDIETA ZUÑIGA',
            'ORGANIZACION_NOMBRE': obj.organizacion.nombre if obj.organizacion else '',
            'FECHA_EMISION': fin.strftime('%d/%m/%Y'),
            'VIGENCIA': fin.replace(year=fin.year + 1).strftime('%d/%m/%Y'),
            'EMPRESA_REPRESENTANTE_LEGAL': 'Nombre representante legal',
            'EMPRESA_REPRESENTANTE_TRABAJADORES': 'Nombre representante trabajadores',
        }

        return ctx, logo_obj

    def _render_docx(self, request, queryset, as_pdf: bool):
        obj = queryset.first()
        if queryset.count() != 1 or obj is None:
            self.message_user(request, 'Selecciona exactamente una plantilla para la vista previa.', level='error')
            return None
        if not obj.archivo or not hasattr(obj.archivo, 'path') or not os.path.exists(obj.archivo.path):
            return HttpResponse('La plantilla seleccionada no tiene archivo subido.', content_type='text/plain; charset=utf-8')

        try:
            from docxtpl import DocxTemplate, InlineImage
            from docx.shared import Mm
        except Exception:
            return HttpResponse('Falta docxtpl. Instala: pip install docxtpl', content_type='text/plain; charset=utf-8')

        ctx, logo_obj = self._build_context(obj)
        doc = DocxTemplate(obj.archivo.path)
        logo_inline = None
        if logo_obj and logo_obj.imagen and hasattr(logo_obj.imagen, 'path') and os.path.exists(logo_obj.imagen.path):
            logo_inline = InlineImage(doc, logo_obj.imagen.path, width=Mm(30))
        ctx['LOGO'] = logo_inline
        # Añadir alias para soportar marcadores alternativos (p. ej., {{ duracion }})
        alias_map = {
            'duracion': 'HORAS',
            'horas': 'HORAS',
            'curso': 'NOMBRE_CURSO',
            'nombre_curso': 'NOMBRE_CURSO',
            'razon_social': 'RAZON_SOCIAL',
            'rfc': 'RFC',
            'instructor': 'INSTRUCTOR_NOMBRE',
            'fecha_emision': 'FECHA_EMISION',
            'vigencia': 'VIGENCIA',
            'logo': 'LOGO',
        }
        ctx_with_aliases = dict(ctx)
        if logo_inline is not None:
            ctx_with_aliases['LOGO'] = logo_inline
        for alias, canonical in alias_map.items():
            if canonical in ctx and alias not in ctx_with_aliases:
                ctx_with_aliases[alias] = ctx[canonical]

        try:
            doc.render(ctx_with_aliases)
        except Exception as exc:
            return HttpResponse(f'Error al renderizar: {exc}', content_type='text/plain; charset=utf-8')

        base_name = f"PREVIEW_{obj.nombre}"
        if as_pdf:
            try:
                with TemporaryDirectory() as tmpdir:
                    docx_out = os.path.join(tmpdir, base_name + '.docx')
                    doc.save(docx_out)
                    from docx2pdf import convert
                    pdf_out = os.path.join(tmpdir, base_name + '.pdf')
                    convert(docx_out, pdf_out)
                    with open(pdf_out, 'rb') as f:
                        data = f.read()
                resp = HttpResponse(data, content_type='application/pdf')
                resp['Content-Disposition'] = f'attachment; filename="{base_name}.pdf"'
                return resp
            except Exception as exc:
                # Fallback a DOCX si falla PDF
                with TemporaryDirectory() as tmpdir:
                    docx_out = os.path.join(tmpdir, base_name + '.docx')
                    doc.save(docx_out)
                    with open(docx_out, 'rb') as f:
                        data = f.read()
                resp = HttpResponse(data, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                resp['Content-Disposition'] = f'attachment; filename="{base_name}.docx"'
                return resp
        else:
            from io import BytesIO
            buf = BytesIO()
            doc.save(buf)
            data = buf.getvalue()
            buf.close()
            resp = HttpResponse(data, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            resp['Content-Disposition'] = f'attachment; filename="{base_name}.docx"'
            return resp

    def vista_previa_docx(self, request, queryset):
        return self._render_docx(request, queryset, as_pdf=False)
    vista_previa_docx.short_description = 'Descargar vista previa DOCX'

    def vista_previa_pdf(self, request, queryset):
        return self._render_docx(request, queryset, as_pdf=True)
    vista_previa_pdf.short_description = 'Descargar vista previa PDF (si es posible)'


@admin.register(LogoDC3)
class LogoDC3Admin(admin.ModelAdmin):
    list_display = ('nombre', 'organizacion', 'empresa', 'activo', 'creado')
    list_filter = ('activo', 'organizacion', 'empresa')
    search_fields = ('nombre', 'organizacion__nombre', 'empresa__nombre')


@admin.register(HistorialCertificadoDC3)
class HistorialCertificadoDC3Admin(admin.ModelAdmin):
    list_display = ('folio', 'codigo_verificacion', 'nombre_completo_alumno', 'nombre_empresa', 'nombre_curso', 'fecha_generacion', 'generado_por')
    list_filter = ('fecha_generacion', 'nombre_empresa', 'horas_curso', 'generado_por')
    search_fields = ('folio', 'codigo_verificacion', 'nombre_completo_alumno', 'curp', 'nombre_empresa', 'nombre_curso')
    readonly_fields = ('folio', 'codigo_verificacion', 'fecha_generacion')
    
    fieldsets = (
                ('Información del Certificado', {
                    'fields': ('folio', 'codigo_verificacion', 'fecha_generacion', 'archivo_pdf_path', 'generado_por')
                }),
        ('Datos del Alumno', {
            'fields': ('nombre_completo_alumno', 'apellido_paterno', 'apellido_materno', 'nombres', 'curp')
        }),
        ('Datos de la Empresa', {
            'fields': ('nombre_empresa', 'rfc_empresa')
        }),
        ('Datos del Curso', {
            'fields': ('nombre_curso', 'horas_curso', 'fecha_inicio', 'fecha_fin', 'instructor_nombre')
        }),
        ('Relaciones', {
            'fields': ('inscripcion',)
        }),
    )
    
    def has_add_permission(self, request):
        # No permitir agregar certificados manualmente desde el admin
        return False
