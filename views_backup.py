from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CursoForm, DC3GenerateForm
from .models import Curso, Inscripcion, Organizacion, Empresa, PlantillaDC3, CertificadoDC3
from django.db.models import Q
from django.core.paginator import Paginator
import csv
from django.utils import timezone
from datetime import timedelta, datetime
import math
import io
import zipfile
from django.conf import settings
import json
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import black, white

# Importaciones para docxtpl
try:
    from docxtpl import DocxTemplate
except ImportError:
    DocxTemplate = None

# Eliminado: mapa de horas y heurísticas para DC-3

@login_required
def crear_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.profesor = request.user
            curso.save()
            return redirect('lista_cursos')
    else:
        form = CursoForm()
    return render(request, 'cursos/crear_curso.html', {'form': form})

@login_required
def editar_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id, profesor=request.user)
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES, instance=curso)
        if form.is_valid():
            form.save()
            return redirect('lista_cursos')
    else:
        form = CursoForm(instance=curso)
    return render(request, 'cursos/editar_curso.html', {'form': form, 'curso': curso})

@login_required
def eliminar_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id, profesor=request.user)
    if request.method == 'POST':
        curso.delete()
        return redirect('lista_cursos')
    return render(request, 'cursos/eliminar_curso.html', {'curso': curso})

def lista_cursos(request):
    queryset = Curso.objects.all().select_related('organizacion', 'profesor')

    # Filtros
    org_id = request.GET.get('org')
    horas_min = request.GET.get('hmin')
    horas_max = request.GET.get('hmax')
    query_text = request.GET.get('q', '')
    sort = request.GET.get('sort', '-fecha')

    if org_id:
        try:
            queryset = queryset.filter(organizacion_id=int(org_id))
        except ValueError:
            pass
    if horas_min:
        try:
            queryset = queryset.filter(duracion_horas__gte=int(horas_min))
        except ValueError:
            pass
    if horas_max:
        try:
            queryset = queryset.filter(duracion_horas__lte=int(horas_max))
        except ValueError:
            pass

    if query_text:
        texto = query_text.strip()
        if texto:
            queryset = queryset.filter(
                Q(nombre__icontains=texto)
                | Q(descripcion__icontains=texto)
                | Q(organizacion__nombre__icontains=texto)
            )

    # Ordenamiento
    sort_map = {
        'nombre': 'nombre',
        '-nombre': '-nombre',
        'horas': 'duracion_horas',
        '-horas': '-duracion_horas',
        'fecha': 'fecha_creacion',
        '-fecha': '-fecha_creacion',
        'organizacion': 'organizacion__nombre',
        '-organizacion': '-organizacion__nombre',
    }
    order_field = sort_map.get(sort, '-fecha_creacion')
    queryset = queryset.order_by(order_field)

    # Exportación CSV manteniendo filtros y orden actual
    export_format = request.GET.get('format')
    if export_format == 'csv':
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="cursos_filtrados.csv"'
        writer = csv.writer(response)
        writer.writerow(['Nombre', 'Organización', 'Horas', 'Profesor', 'Fecha creación'])
        for c in queryset:
            writer.writerow([
                c.nombre,
                c.organizacion.nombre if c.organizacion else '',
                c.duracion_horas or '',
                getattr(c.profesor, 'username', ''),
                c.fecha_creacion.strftime('%Y-%m-%d %H:%M'),
            ])
        return response

    organizaciones = Organizacion.objects.all().order_by('nombre')
    # Paginación
    per_page_raw = request.GET.get('per_page') or '12'
    try:
        per_page = max(1, min(60, int(per_page_raw)))
    except ValueError:
        per_page = 12
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page') or 1
    page_obj = paginator.get_page(page_number)

    # Querystring sin el parámetro de página, para reutilizar en enlaces
    params = request.GET.copy()
    params.pop('page', None)
    querystring_no_page = params.urlencode()

    context = {
        'cursos': page_obj.object_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'organizaciones': organizaciones,
        'selected_org': org_id or '',
        'hmin': horas_min or '',
        'hmax': horas_max or '',
        'q': query_text or '',
        'sort': sort,
        'per_page': per_page,
        'querystring_no_page': querystring_no_page,
        'total': paginator.count,
    }
    return render(request, 'cursos/lista_cursos.html', context)

def detalle_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    
    # Si el usuario no está autenticado, mostrar página de registro
    if not request.user.is_authenticated:
        return render(request, 'cursos/registro_requerido.html', {'curso': curso})
    
    # Verificar si el usuario está inscrito en este curso y si ya tiene certificado
    inscripcion = None
    certificado_existe = False
    certificado_info = None
    
    if request.user.is_authenticated:
        inscripcion = Inscripcion.objects.filter(
            alumno=request.user, 
            curso=curso
        ).first()
        
        if inscripcion:
            certificado_existe = CertificadoDC3.objects.filter(inscripcion=inscripcion).exists()
            if certificado_existe:
                certificado = CertificadoDC3.objects.get(inscripcion=inscripcion)
                certificado_info = {
                    'fecha_generacion': certificado.fecha_emision.strftime('%d/%m/%Y'),
                    'folio': f"DC3-{certificado.fecha_emision.year}-{certificado.id:05d}"
                }
    
    context = {
        'curso': curso,
        'inscripcion': inscripcion,
        'certificado_existe': certificado_existe,
        'certificado_info': certificado_info
    }
    
    return render(request, 'cursos/detalle_curso.html', context)

@login_required
def inscribirse_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    
    print(f"DEBUG - Usuario: {request.user.username}")
    print(f"DEBUG - Curso: {curso.nombre} (ID: {curso.id})")
    
    # Verificar si ya está inscrito
    if Inscripcion.objects.filter(alumno=request.user, curso=curso).exists():
        print(f"DEBUG - Usuario ya inscrito en este curso")
        return redirect('mis_cursos')
    
    if request.method == 'POST':
        print(f"DEBUG - Creando inscripción...")
        inscripcion = Inscripcion.objects.create(
            alumno=request.user,
            curso=curso,
            fecha_inscripcion=timezone.now()
        )
        print(f"DEBUG - Inscripción creada con ID: {inscripcion.id}")
        
        # NO generar automáticamente el certificado - el usuario lo generará manualmente
        print(f"DEBUG - Inscripción completada. El usuario puede generar el certificado manualmente.")
        
        # Agregar mensaje de éxito
        messages.success(request, f'Te has inscrito exitosamente al curso "{curso.nombre}". Ahora puedes generar tu certificado DC-3.')
        
        return redirect('mis_cursos')
        
        # CÓDIGO COMENTADO - Generación automática deshabilitada
        # try:
        #     # Obtener datos del usuario
        #     user = request.user
            nombres = user.first_name or ''
            apellidos = user.last_name or ''
            
            # Separar apellidos si están juntos
            if apellidos:
                apellidos_list = apellidos.split()
                if len(apellidos_list) >= 2:
                    apellido_paterno = apellidos_list[0]
                    apellido_materno = ' '.join(apellidos_list[1:])
                else:
                    apellido_paterno = apellidos_list[0]
                    apellido_materno = ''
            else:
                apellido_paterno = ''
                apellido_materno = ''
            
            # Crear datos para el certificado
            data = {
                'apellido_paterno': apellido_paterno,
                'apellido_materno': apellido_materno,
                'nombres': nombres,
                'curp': user.curp if hasattr(user, 'curp') else '',
                'puesto': user.puesto if hasattr(user, 'puesto') else 'EMPLEADO',
                'nombre_curso': curso.nombre,  # NOMBRE DEL CURSO DONDE SE INSCRIBIÓ
                'horas_curso': str(curso.duracion_horas) if curso.duracion_horas else '0',
                'nombre_empresa': user.empresa.nombre if hasattr(user, 'empresa') and user.empresa else 'EMPRESA',
                'rfc_empresa': user.empresa.rfc if hasattr(user, 'empresa') and user.empresa else 'RFC',
                'representante_legal': user.representante_legal if hasattr(user, 'representante_legal') else 'REPRESENTANTE LEGAL',
                'representante_trabajadores': user.representante_trabajadores if hasattr(user, 'representante_trabajadores') else 'REPRESENTANTE TRABAJADORES',
                'fecha_inicio': curso.fecha_creacion.date(),
                'fecha_fin': curso.fecha_creacion.date(),
                'instructor_nombre': curso.profesor.get_full_name() if curso.profesor else 'INSTRUCTOR',
            }
            
            print(f"DEBUG - Nombre del curso: {curso.nombre}")
            print(f"DEBUG - Datos del certificado: {data}")
            
            # Obtener la plantilla según la organización del curso
            if curso.organizacion and curso.organizacion.nombre == "Fraternidad Migratoria":
                plantilla_id = 10  # Plantilla de Fraternidad Migratoria
            elif curso.organizacion and curso.organizacion.nombre == "CPI":
                plantilla_id = 11  # Plantilla de CPI
            else:
                # Fallback a Fraternidad Migratoria si no hay organización o es otra
                plantilla_id = 10
            
            # Coordenadas para caracteres individuales (las que configuraste)
            coordenadas_caracteres = {
                # CURP (18 caracteres)
                'curp_0': (43, 593), 'curp_1': (58, 593), 'curp_2': (72, 593), 'curp_3': (88, 593),
                'curp_4': (102, 593), 'curp_5': (117, 593), 'curp_6': (132, 593), 'curp_7': (145, 593),
                'curp_8': (158, 593), 'curp_9': (172, 593), 'curp_10': (187, 593), 'curp_11': (201, 593),
                'curp_12': (217, 593), 'curp_13': (233, 593), 'curp_14': (250, 593), 'curp_15': (265, 593),
                'curp_16': (279, 593), 'curp_17': (297, 593),
                
                # RFC (13 caracteres)
                'rfc_0': (45, 496), 'rfc_1': (58, 496), 'rfc_2': (72, 496), 'rfc_3': (90, 496),
                'rfc_4': (118, 496), 'rfc_5': (132, 496), 'rfc_6': (144, 496), 'rfc_7': (157, 496),
                'rfc_8': (172, 496), 'rfc_9': (186, 496), 'rfc_10': (217, 496), 'rfc_11': (233, 496),
                'rfc_12': (250, 496),
                
                # Fecha Inicio (solo las posiciones con coordenadas válidas)
                'fecha_ini_0': (260, 416), 'fecha_ini_1': (277, 416), 'fecha_ini_2': (292, 416),
                'fecha_ini_3': (308, 416), 'fecha_ini_5': (327, 416), 'fecha_ini_6': (347, 416),
                'fecha_ini_8': (368, 416), 'fecha_ini_9': (390, 416),
                
                # Fecha Fin (solo las posiciones con coordenadas válidas)
                'fecha_fin_0': (431, 416), 'fecha_fin_1': (450, 416), 'fecha_fin_2': (470, 416),
                'fecha_fin_3': (487, 416), 'fecha_fin_5': (510, 416), 'fecha_fin_6': (530, 416),
                'fecha_fin_8': (550, 416), 'fecha_fin_9': (570, 416)
            }
            
            # Generar el certificado
            pdf_content = generar_pdf_con_caracteres_individuales(data, plantilla_id, coordenadas_caracteres)
            
            # Crear registro de certificado DC-3
            from .models import CertificadoDC3, Empresa
            
            # Obtener o crear empresa por defecto
            empresa_default, created = Empresa.objects.get_or_create(
                nombre='EMPRESA',
                defaults={
                    'rfc': 'RFC',
                    'representante_legal': 'REPRESENTANTE LEGAL',
                    'representante_trabajadores': 'REPRESENTANTE TRABAJADORES'
                }
            )
            
            # Verificar si ya existe un certificado para esta inscripción
            if CertificadoDC3.objects.filter(inscripcion=inscripcion).exists():
                print(f"DEBUG - Ya existe un certificado para esta inscripción: {inscripcion.id}")
                return redirect('mis_cursos')
            
            # Crear el certificado
            certificado = CertificadoDC3.objects.create(
                inscripcion=inscripcion,
                empresa=empresa_default,
                apellido_paterno=apellido_paterno,
                apellido_materno=apellido_materno,
                nombres=nombres,
                nombre_completo=f"{apellido_paterno} {apellido_materno} {nombres}".strip(),
                curp=data['curp'],
                puesto=data['puesto'],
                horas_curso=curso.duracion_horas if curso.duracion_horas else 4
            )
            
            # Guardar el PDF en el certificado
            from django.core.files.base import ContentFile
            nombre_archivo = f"DC3_{apellido_paterno}_{apellido_materno}_{nombres}_{curso.nombre}_{timezone.now().strftime('%Y%m%d')}.pdf"
            certificado.archivo_pdf.save(nombre_archivo, ContentFile(pdf_content), save=True)
            
            print(f"Certificado generado automáticamente para {user.username} en curso {curso.nombre}")
            print(f"PDF guardado como: {certificado.archivo_pdf.name}")
            
            print(f"Certificado generado automáticamente para {user.username} en curso {curso.nombre}")
            
        except Exception as e:
            print(f"Error al generar certificado automático: {e}")
        
        return redirect('mis_cursos')
    
    return render(request, 'cursos/inscribirse_curso.html', {'curso': curso})

@login_required
def mis_cursos(request):
    print(f"DEBUG - Usuario solicitando mis_cursos: {request.user.username}")
    inscripciones = Inscripcion.objects.filter(alumno=request.user).select_related('curso', 'curso__organizacion', 'certificado')
    print(f"DEBUG - Inscripciones encontradas: {inscripciones.count()}")
    for inscripcion in inscripciones:
        print(f"DEBUG - Inscripción: {inscripcion.curso.nombre} - {inscripcion.fecha_inscripcion}")
    
    # Contar certificados generados
    certificados_generados = sum(1 for inscripcion in inscripciones if hasattr(inscripcion, 'certificado'))
    
    context = {
        'inscripciones': inscripciones,
        'certificados_generados': certificados_generados,
        'total_inscripciones': inscripciones.count()
    }
    
    return render(request, 'cursos/mis_cursos.html', context)


@login_required
def descargar_plantilla_pdf(request, tipo_plantilla):
    """
    Vista para descargar plantillas PDF para que los alumnos las llenen manualmente
    """
    if tipo_plantilla == 'fraternidad':
        filename = 'CERTIFICADO_DC-3_FRATERNIDAD_MIGRATORIA.pdf'
        template_path = os.path.join(settings.MEDIA_ROOT, 'plantillas', 'dc3', filename)
    elif tipo_plantilla == 'cpi':
        filename = 'CERTIFICADO_DC3_cpi.pdf'
        template_path = os.path.join(settings.MEDIA_ROOT, 'plantillas', 'dc3', filename)
    else:
        return HttpResponse('Tipo de plantilla no válido', status=400)
    
    if not os.path.exists(template_path):
        return HttpResponse(f'Plantilla {filename} no encontrada', status=404)
    
    try:
        with open(template_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    except Exception as e:
        return HttpResponse(f'Error al descargar la plantilla: {str(e)}', status=500)



def procesar_pdf_llenado(request):
    """
    Vista para procesar formularios PDF llenados por los alumnos
    """
    if request.method == 'POST':
        # Aquí procesarías el PDF llenado
        # Por ahora, solo un placeholder
        return HttpResponse('Funcionalidad de procesamiento PDF en desarrollo')
    
    # Obtener lista de cursos para el formulario
    cursos = Curso.objects.all()
    return render(request, 'cursos/procesar_pdf.html', {'cursos': cursos})



# Funciones de certificados eliminadas - ahora se usa el nuevo sistema de generación DC-3

def generar_pdf_con_campos_editables(data, plantilla_choice):
    """
    Genera un PDF con campos de formulario editables usando ReportLab
    """
    import io
    
    # Crear buffer para el PDF
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=A4)
    
    # Configurar fuentes
    c.setFont("Helvetica-Bold", 16)
    
    # Título del certificado
    c.drawString(150, 750, "CERTIFICADO DE COMPETENCIAS LABORALES DC-3")
    c.setFont("Helvetica", 12)
    
    # Marco del certificado
    c.rect(30, 30, 550, 720)
    
    # Información del trabajador
    y_position = 700
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "INFORMACIÓN DEL TRABAJADOR:")
    c.setFont("Helvetica", 10)
    
    y_position -= 25
    c.drawString(50, y_position, f"Apellido Paterno: {data['apellido_paterno']}")
    y_position -= 20
    c.drawString(50, y_position, f"Apellido Materno: {data['apellido_materno']}")
    y_position -= 20
    c.drawString(50, y_position, f"Nombres: {data['nombres']}")
    y_position -= 20
    c.drawString(50, y_position, f"CURP: {data['curp']}")
    y_position -= 20
    c.drawString(50, y_position, f"Puesto: {data['puesto']}")
    y_position -= 20
    c.drawString(50, y_position, f"Ocupación: {data['ocupacion']}")
    
    # Información del curso
    y_position -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "INFORMACIÓN DEL CURSO:")
    c.setFont("Helvetica", 10)
    
    y_position -= 25
    c.drawString(50, y_position, f"Nombre del Curso: {data['nombre_curso']}")
    y_position -= 20
    c.drawString(50, y_position, f"Horas: {data['horas_curso']}")
    y_position -= 20
    c.drawString(50, y_position, f"Área Temática: {data['area_tematica']}")
    
    # Fechas
    y_position -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "FECHAS DEL CURSO:")
    c.setFont("Helvetica", 10)
    
    y_position -= 25
    c.drawString(50, y_position, f"Fecha de Inicio: {data['fecha_inicio'].strftime('%d/%m/%Y')}")
    y_position -= 20
    c.drawString(50, y_position, f"Fecha de Finalización: {data['fecha_fin'].strftime('%d/%m/%Y')}")
    
    # Información de la empresa
    y_position -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "INFORMACIÓN DE LA EMPRESA:")
    c.setFont("Helvetica", 10)
    
    y_position -= 25
    c.drawString(50, y_position, f"Razón Social: {data['nombre_empresa']}")
    y_position -= 20
    c.drawString(50, y_position, f"RFC: {data['rfc_empresa']}")
    y_position -= 20
    c.drawString(50, y_position, f"Representante Legal: {data['representante_legal']}")
    y_position -= 20
    c.drawString(50, y_position, f"Representante de Trabajadores: {data['representante_trabajadores']}")
    
    # Información del instructor
    y_position -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "INFORMACIÓN DEL INSTRUCTOR:")
    c.setFont("Helvetica", 10)
    
    y_position -= 25
    c.drawString(50, y_position, f"Instructor: {data['instructor_nombre']}")
    
    # Fecha de emisión
    y_position -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "FECHA DE EMISIÓN:")
    c.setFont("Helvetica", 10)
    
    y_position -= 25
    c.drawString(50, y_position, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}")
    
    # Campos editables para información adicional
    y_position -= 50
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "CAMPOS EDITABLES:")
    c.setFont("Helvetica", 10)
    
    # Campo editable para observaciones
    y_position -= 30
    c.drawString(50, y_position, "Observaciones:")
    c.rect(50, y_position-25, 500, 30)
    c.setFont("Helvetica", 8)
    c.drawString(55, y_position-15, "Haga clic aquí para agregar observaciones")
    
    # Campo editable para información adicional
    y_position -= 50
    c.setFont("Helvetica", 10)
    c.drawString(50, y_position, "Información Adicional:")
    c.rect(50, y_position-25, 500, 30)
    c.setFont("Helvetica", 8)
    c.drawString(55, y_position-15, "Haga clic aquí para agregar información adicional")
    
    # Espacios para firma y sello
    y_position -= 80
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "FIRMAS Y SELLOS:")
    c.setFont("Helvetica", 10)
    
    # Espacio para firma del instructor
    y_position -= 30
    c.drawString(50, y_position, "Firma del Instructor:")
    c.rect(50, y_position-40, 200, 50)
    c.setFont("Helvetica", 8)
    c.drawString(55, y_position-20, "Espacio para firma")
    
    # Espacio para sello
    c.drawString(300, y_position, "Sello:")
    c.rect(300, y_position-40, 200, 50)
    c.setFont("Helvetica", 8)
    c.drawString(305, y_position-20, "Espacio para sello")
    
    # Espacio para firma del representante
    y_position -= 80
    c.setFont("Helvetica", 10)
    c.drawString(50, y_position, "Firma del Representante Legal:")
    c.rect(50, y_position-40, 200, 50)
    c.setFont("Helvetica", 8)
    c.drawString(55, y_position-20, "Espacio para firma")
    
    # Información de la organización
    y_position -= 60
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y_position, "ORGANIZACIÓN:")
    c.setFont("Helvetica", 10)
    c.drawString(50, y_position-20, "ICCSI - Instituto de Capacitación y Certificación")
    c.drawString(50, y_position-35, "Agente Capacitador: Fraternidad Migratoria A.C.")
    c.drawString(50, y_position-50, "Registro: Fmi111006-4q2-0013")
    
    c.save()
    
    # Obtener el contenido del PDF
    pdf_buffer.seek(0)
    pdf_content = pdf_buffer.getvalue()
    pdf_buffer.close()
    
    return pdf_content

def generar_pdf_con_formulario_editable(data, plantilla_choice):
    """
    Genera un PDF con campos de formulario reales que se pueden llenar
    """
    import io
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.colors import black, white, blue
    
    # Crear buffer para el PDF
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=A4)
    
    # Configurar fuentes
    c.setFont("Helvetica-Bold", 16)
    
    # Título del certificado
    c.drawString(150, 750, "CERTIFICADO DE COMPETENCIAS LABORALES DC-3")
    c.setFont("Helvetica", 12)
    
    # Marco del certificado
    c.rect(30, 30, 550, 720)
    
    # Información del trabajador
    y_position = 700
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "INFORMACIÓN DEL TRABAJADOR:")
    c.setFont("Helvetica", 10)
    
    y_position -= 25
    c.drawString(50, y_position, f"Apellido Paterno: {data['apellido_paterno']}")
    y_position -= 20
    c.drawString(50, y_position, f"Apellido Materno: {data['apellido_materno']}")
    y_position -= 20
    c.drawString(50, y_position, f"Nombres: {data['nombres']}")
    y_position -= 20
    c.drawString(50, y_position, f"CURP: {data['curp']}")
    y_position -= 20
    c.drawString(50, y_position, f"Puesto: {data['puesto']}")
    y_position -= 20
    c.drawString(50, y_position, f"Ocupación: {data['ocupacion']}")
    
    # Información del curso
    y_position -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "INFORMACIÓN DEL CURSO:")
    c.setFont("Helvetica", 10)
    
    y_position -= 25
    c.drawString(50, y_position, f"Nombre del Curso: {data['nombre_curso']}")
    y_position -= 20
    c.drawString(50, y_position, f"Horas: {data['horas_curso']}")
    y_position -= 20
    c.drawString(50, y_position, f"Área Temática: {data['area_tematica']}")
    
    # Fechas
    y_position -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "FECHAS DEL CURSO:")
    c.setFont("Helvetica", 10)
    
    y_position -= 25
    c.drawString(50, y_position, f"Fecha de Inicio: {data['fecha_inicio'].strftime('%d/%m/%Y')}")
    y_position -= 20
    c.drawString(50, y_position, f"Fecha de Finalización: {data['fecha_fin'].strftime('%d/%m/%Y')}")
    
    # Información de la empresa
    y_position -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "INFORMACIÓN DE LA EMPRESA:")
    c.setFont("Helvetica", 10)
    
    y_position -= 25
    c.drawString(50, y_position, f"Razón Social: {data['nombre_empresa']}")
    y_position -= 20
    c.drawString(50, y_position, f"RFC: {data['rfc_empresa']}")
    y_position -= 20
    c.drawString(50, y_position, f"Representante Legal: {data['representante_legal']}")
    y_position -= 20
    c.drawString(50, y_position, f"Representante de Trabajadores: {data['representante_trabajadores']}")
    
    # Información del instructor
    y_position -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "INFORMACIÓN DEL INSTRUCTOR:")
    c.setFont("Helvetica", 10)
    
    y_position -= 25
    c.drawString(50, y_position, f"Instructor: {data['instructor_nombre']}")
    
    # Fecha de emisión
    y_position -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "FECHA DE EMISIÓN:")
    c.setFont("Helvetica", 10)
    
    y_position -= 25
    c.drawString(50, y_position, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}")
    
    # Campos de formulario editables
    y_position -= 50
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "CAMPOS EDITABLES:")
    c.setFont("Helvetica", 10)
    
    # Campo de texto para observaciones
    y_position -= 30
    c.drawString(50, y_position, "Observaciones:")
    # Crear campo de texto editable
    c.rect(50, y_position-25, 500, 30, fill=0)
    c.setFont("Helvetica", 8)
    c.drawString(55, y_position-15, "Campo editable - haga clic para escribir")
    
    # Campo de texto para información adicional
    y_position -= 50
    c.setFont("Helvetica", 10)
    c.drawString(50, y_position, "Información Adicional:")
    c.rect(50, y_position-25, 500, 30, fill=0)
    c.setFont("Helvetica", 8)
    c.drawString(55, y_position-15, "Campo editable - haga clic para escribir")
    
    # Espacios para firma y sello
    y_position -= 80
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "FIRMAS Y SELLOS:")
    c.setFont("Helvetica", 10)
    
    # Espacio para firma del instructor
    y_position -= 30
    c.drawString(50, y_position, "Firma del Instructor:")
    c.rect(50, y_position-40, 200, 50, fill=0)
    c.setFont("Helvetica", 8)
    c.drawString(55, y_position-20, "Espacio para firma")
    
    # Espacio para sello
    c.drawString(300, y_position, "Sello:")
    c.rect(300, y_position-40, 200, 50, fill=0)
    c.setFont("Helvetica", 8)
    c.drawString(305, y_position-20, "Espacio para sello")
    
    # Espacio para firma del representante
    y_position -= 80
    c.setFont("Helvetica", 10)
    c.drawString(50, y_position, "Firma del Representante Legal:")
    c.rect(50, y_position-40, 200, 50, fill=0)
    c.setFont("Helvetica", 8)
    c.drawString(55, y_position-20, "Espacio para firma")
    
    # Información de la organización
    y_position -= 60
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y_position, "ORGANIZACIÓN:")
    c.setFont("Helvetica", 10)
    c.drawString(50, y_position-20, "ICCSI - Instituto de Capacitación y Certificación")
    c.drawString(50, y_position-35, "Agente Capacitador: Fraternidad Migratoria A.C.")
    c.drawString(50, y_position-50, "Registro: Fmi111006-4q2-0013")
    
    # Agregar instrucciones para el usuario
    y_position -= 80
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y_position, "INSTRUCCIONES:")
    c.setFont("Helvetica", 8)
    c.drawString(50, y_position-15, "1. Este PDF se puede llenar directamente en cualquier lector de PDF")
    c.drawString(50, y_position-30, "2. Haga clic en los campos marcados para agregar información")
    c.drawString(50, y_position-45, "3. Guarde el archivo después de llenarlo")
    c.drawString(50, y_position-60, "4. El archivo es oficial y válido para trámites laborales")
    
    c.save()
    
    # Obtener el contenido del PDF
    pdf_buffer.seek(0)
    pdf_content = pdf_buffer.getvalue()
    pdf_buffer.close()
    
    return pdf_content

def generar_plantilla_pdf_vacia(tipo_plantilla):
    """
    Genera una plantilla PDF vacía que se puede llenar manualmente
    """
    import io
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.colors import black, white, blue
    
    # Crear buffer para el PDF
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=A4)
    
    # Configurar fuentes
    c.setFont("Helvetica-Bold", 16)
    
    # Título del certificado
    if tipo_plantilla == 'fraternidad':
        c.drawString(150, 750, "CERTIFICADO DE COMPETENCIAS LABORALES DC-3")
        c.drawString(200, 730, "FRATERNIDAD MIGRATORIA A.C.")
    else:
        c.drawString(150, 750, "CERTIFICADO DE COMPETENCIAS LABORALES DC-3")
        c.drawString(200, 730, "CPI - CENTRO DE POBLACIÓN")
    
    c.setFont("Helvetica", 12)
    
    # Marco del certificado
    c.rect(30, 30, 550, 720)
    
    # Información del trabajador
    y_position = 700
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "INFORMACIÓN DEL TRABAJADOR:")
    c.setFont("Helvetica", 10)
    
    y_position -= 25
    c.drawString(50, y_position, "Apellido Paterno: _________________________")
    y_position -= 20
    c.drawString(50, y_position, "Apellido Materno: _________________________")
    y_position -= 20
    c.drawString(50, y_position, "Nombres: _________________________")
    y_position -= 20
    c.drawString(50, y_position, "CURP: _________________________")
    y_position -= 20
    c.drawString(50, y_position, "Puesto: _________________________")
    y_position -= 20
    c.drawString(50, y_position, "Ocupación: _________________________")
    
    # Información del curso
    y_position -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "INFORMACIÓN DEL CURSO:")
    c.setFont("Helvetica", 10)
    
    y_position -= 25
    c.drawString(50, y_position, "Nombre del Curso: _________________________")
    y_position -= 20
    c.drawString(50, y_position, "Horas: _________________________")
    y_position -= 20
    c.drawString(50, y_position, "Área Temática: _________________________")
    
    # Fechas
    y_position -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "FECHAS DEL CURSO:")
    c.setFont("Helvetica", 10)
    
    y_position -= 25
    c.drawString(50, y_position, "Fecha de Inicio: _________________________")
    y_position -= 20
    c.drawString(50, y_position, "Fecha de Finalización: _________________________")
    
    # Información de la empresa
    y_position -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "INFORMACIÓN DE LA EMPRESA:")
    c.setFont("Helvetica", 10)
    
    y_position -= 25
    c.drawString(50, y_position, "Razón Social: _________________________")
    y_position -= 20
    c.drawString(50, y_position, "RFC: _________________________")
    y_position -= 20
    c.drawString(50, y_position, "Representante Legal: _________________________")
    y_position -= 20
    c.drawString(50, y_position, "Representante de Trabajadores: _________________________")
    
    # Información del instructor
    y_position -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "INFORMACIÓN DEL INSTRUCTOR:")
    c.setFont("Helvetica", 10)
    
    y_position -= 25
    c.drawString(50, y_position, "Instructor: _________________________")
    
    # Fecha de emisión
    y_position -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "FECHA DE EMISIÓN:")
    c.setFont("Helvetica", 10)
    
    y_position -= 25
    c.drawString(50, y_position, "Fecha: _________________________")
    
    # Campos para llenar manualmente
    y_position -= 50
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "CAMPOS PARA LLENAR:")
    c.setFont("Helvetica", 10)
    
    # Campo para observaciones
    y_position -= 30
    c.drawString(50, y_position, "Observaciones:")
    c.rect(50, y_position-25, 500, 30, fill=0)
    c.setFont("Helvetica", 8)
    c.drawString(55, y_position-15, "Escriba aquí las observaciones")
    
    # Campo para información adicional
    y_position -= 50
    c.setFont("Helvetica", 10)
    c.drawString(50, y_position, "Información Adicional:")
    c.rect(50, y_position-25, 500, 30, fill=0)
    c.setFont("Helvetica", 8)
    c.drawString(55, y_position-15, "Escriba aquí información adicional")
    
    # Espacios para firma y sello
    y_position -= 80
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "FIRMAS Y SELLOS:")
    c.setFont("Helvetica", 10)
    
    # Espacio para firma del instructor
    y_position -= 30
    c.drawString(50, y_position, "Firma del Instructor:")
    c.rect(50, y_position-40, 200, 50, fill=0)
    c.setFont("Helvetica", 8)
    c.drawString(55, y_position-20, "Espacio para firma")
    
    # Espacio para sello
    c.drawString(300, y_position, "Sello:")
    c.rect(300, y_position-40, 200, 50, fill=0)
    c.setFont("Helvetica", 8)
    c.drawString(305, y_position-20, "Espacio para sello")
    
    # Espacio para firma del representante
    y_position -= 80
    c.setFont("Helvetica", 10)
    c.drawString(50, y_position, "Firma del Representante Legal:")
    c.rect(50, y_position-40, 200, 50, fill=0)
    c.setFont("Helvetica", 8)
    c.drawString(55, y_position-20, "Espacio para firma")
    
    # Información de la organización
    y_position -= 60
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y_position, "ORGANIZACIÓN:")
    c.setFont("Helvetica", 10)
    c.drawString(50, y_position-20, "ICCSI - Instituto de Capacitación y Certificación")
    c.drawString(50, y_position-35, "Agente Capacitador: Fraternidad Migratoria A.C.")
    c.drawString(50, y_position-50, "Registro: Fmi111006-4q2-0013")
    
    # Instrucciones
    y_position -= 80
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y_position, "INSTRUCCIONES:")
    c.setFont("Helvetica", 8)
    c.drawString(50, y_position-15, "1. Complete todos los campos marcados con líneas")
    c.drawString(50, y_position-30, "2. Escriba claramente en los espacios proporcionados")
    c.drawString(50, y_position-45, "3. Agregue firmas y sellos en los espacios correspondientes")
    c.drawString(50, y_position-60, "4. Este documento es oficial para trámites laborales")
    
    c.save()
    
    # Obtener el contenido del PDF
    pdf_buffer.seek(0)
    pdf_content = pdf_buffer.getvalue()
    pdf_buffer.close()
    
    return pdf_content

@login_required
def llenar_pdf_en_sistema(request, certificado_id=None):
    """
    Redirige a la vista principal de generación de certificados DC-3
    """
    from django.shortcuts import redirect
    return redirect('llenar_plantilla_dc3_sistema')

def generar_pdf_final_con_firma(data, plantilla_id=None):
    """
    Genera un PDF usando la plantilla seleccionada o un PDF básico como fallback
    """
    if plantilla_id:
        try:
            return generar_pdf_con_plantilla(data, plantilla_id)
        except Exception as e:
            print(f"Error al usar plantilla: {e}")
            print("Usando PDF básico como fallback...")
    
    return generar_pdf_basico(data)

def generar_pdf_con_plantilla(data, plantilla_id, coordenadas_personalizadas=None):
    """
    Genera un PDF usando la plantilla PDF seleccionada de Fraternidad Migratoria
    """
    from PyPDF2 import PdfReader, PdfWriter
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.colors import black
    import io
    from datetime import datetime
    
    # Obtener la plantilla
    plantilla = PlantillaDC3.objects.get(id=plantilla_id, activo=True)
    
    # Leer la plantilla PDF
    with open(plantilla.archivo.path, 'rb') as template_file:
        template_reader = PdfReader(template_file)
        template_page = template_reader.pages[0]
        
        # Crear un nuevo PDF con los datos
        output = PdfWriter()
        
        # Crear un PDF temporal con los datos del formulario
        data_pdf = io.BytesIO()
        c = canvas.Canvas(data_pdf)
        
        # Configurar fuente y tamaño
        c.setFont("Helvetica", 10)
        
        # COORDENADAS - USAR PERSONALIZADAS SI SE PROPORCIONAN
        # ===================================================
        if coordenadas_personalizadas:
            posiciones = coordenadas_personalizadas
        else:
            # COORDENADAS ACTUALIZADAS CON LAS QUE CONFIGURASTE
            # ===================================================
                                posiciones = {
                        'nombres': (225, 620),
                        'apellido_paterno': (225, 620),
                        'apellido_materno': (225, 620),
                        'curp': (43, 593),
                        'puesto': (77, 578),
                        'nombre_curso': (114, 450),
                        'horas_curso': (54, 416),
                        'nombre_empresa': (200, 525),
                        'rfc_empresa': (43, 496),
                        'representante_legal': (225, 302),
                        'representante_trabajadores': (400, 302),
                        'fecha_inicio': (257, 416),
                        'fecha_fin': (427, 416),
                        'instructor_nombre': (50, 302),
                    }
        
        # Escribir los datos en el PDF
        for campo, (x, y) in posiciones.items():
            if campo == 'nombres':
                # Combinar nombre completo: APELLIDOS + NOMBRES
                apellido_paterno = data.get('apellido_paterno', '')
                apellido_materno = data.get('apellido_materno', '')
                nombres = data.get('nombres', '')
                nombre_completo = f"{apellido_paterno} {apellido_materno} {nombres}".strip()
                c.drawString(x, y, nombre_completo)
            
            elif campo == 'curp':
                # CURP - escribir como texto normal (SIN CARACTERES INDIVIDUALES)
                curp = str(data.get('curp', '')).upper()
                c.drawString(x, y, curp)
            
            elif campo == 'rfc_empresa':
                # RFC - escribir como texto normal (SIN CARACTERES INDIVIDUALES)
                rfc = str(data.get('rfc_empresa', '')).upper()
                c.drawString(x, y, rfc)
            
            elif campo in ['fecha_inicio', 'fecha_fin']:
                # Fechas - formato YYYYMMDD (SIN BARRAS)
                if hasattr(data.get(campo), 'strftime'):
                    fecha_str = data.get(campo).strftime('%Y%m%d')  # SIN BARRAS
                else:
                    fecha_str = str(data.get(campo, '')).replace('/', '')
                c.drawString(x, y, fecha_str)
            
            elif campo == 'nombre_curso':
                # Manejar texto largo del curso con múltiples líneas
                valor = data.get(campo, '')
                
                # Configuración para el recuadro del curso
                ancho_maximo = 490  # Ancho máximo del recuadro (optimizado)
                alto_linea = 11     # Altura entre líneas (optimizada)
                fuente_base = 8     # Tamaño de fuente base (reducido)
                
                # Dividir el texto en palabras
                palabras = valor.split()
                lineas = []
                linea_actual = ""
                
                for palabra in palabras:
                    # Probar si la palabra cabe en la línea actual
                    texto_prueba = linea_actual + " " + palabra if linea_actual else palabra
                    c.setFont("Helvetica", fuente_base)
                    ancho_texto = c.stringWidth(texto_prueba, "Helvetica", fuente_base)
                    
                    if ancho_texto <= ancho_maximo:
                        linea_actual = texto_prueba
                    else:
                        if linea_actual:
                            lineas.append(linea_actual)
                        linea_actual = palabra
                
                # Agregar la última línea
                if linea_actual:
                    lineas.append(linea_actual)
                
                # Si no hay líneas, usar el texto original
                if not lineas:
                    lineas = [valor]
                
                # Escribir cada línea
                for i, linea in enumerate(lineas):
                    y_linea = y - (i * alto_linea)
                    c.setFont("Helvetica", fuente_base)
                    c.drawString(x, y_linea, linea)
                
                # Restablecer la fuente a la predeterminada
                c.setFont("Helvetica", 10)
            
            else:
                # Otros campos normales
                valor = data.get(campo, '')
                if hasattr(valor, 'strftime'):  # Verificar si es una fecha
                    valor = valor.strftime('%d/%m/%Y')
                c.drawString(x, y, str(valor))
        
        c.save()
        data_pdf.seek(0)
        
        # Combinar la plantilla con los datos
        data_reader = PdfReader(data_pdf)
        data_page = data_reader.pages[0]
        
        # Superponer los datos sobre la plantilla
        template_page.merge_page(data_page)
        output.add_page(template_page)
        
        # Proteger el PDF con contraseña
        # output = proteger_pdf_con_contraseña(output)  # DESHABILITADO para permitir extracción de texto
        
        # Generar el PDF final
        result_pdf = io.BytesIO()
        output.write(result_pdf)
        result_pdf.seek(0)
        
        return result_pdf.getvalue()

def generar_pdf_basico(data):
    """
    Genera un PDF básico desde cero con formato profesional
    """
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.utils import ImageReader
    from reportlab.lib.colors import black, white
    import io
    import base64
    from datetime import datetime
    
    # Crear buffer para el PDF
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=A4)
    
    # Configurar colores
    c.setFillColor(black)
    
    # Título principal
    c.setFont("Helvetica-Bold", 18)
    c.drawString(150, 750, "CERTIFICADO DE COMPETENCIAS LABORALES DC-3")
    
    # Subtítulo
    c.setFont("Helvetica-Bold", 14)
    c.drawString(200, 720, "CONSTANCIA DE COMPETENCIAS O DE HABILIDADES LABORALES")
    
    # Marco del certificado
    c.rect(30, 30, 550, 720)
    
    # Línea separadora
    c.line(30, 700, 580, 700)
    
    # Información del trabajador
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 670, "DATOS DEL TRABAJADOR:")
    c.setFont("Helvetica", 10)
    
    # Nombre completo
    nombre_completo = f"{data.get('apellido_paterno', '')} {data.get('apellido_materno', '')} {data.get('nombres', '')}".strip()
    c.drawString(50, 650, f"Nombre: {nombre_completo}")
    
    # CURP
    c.drawString(50, 630, f"CURP: {data.get('curp', '')}")
    
    # Puesto
    c.drawString(50, 610, f"Puesto: {data.get('puesto', '')}")
    
    # Ocupación
    c.drawString(50, 590, f"Ocupación: {data.get('ocupacion', '')}")
    
    # Línea separadora
    c.line(30, 570, 580, 570)
    
    # Información de la empresa
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 550, "DATOS DE LA EMPRESA:")
    c.setFont("Helvetica", 10)
    
    c.drawString(50, 530, f"Empresa: {data.get('nombre_empresa', '')}")
    c.drawString(50, 510, f"RFC: {data.get('rfc_empresa', '')}")
    
    # Línea separadora
    c.line(30, 490, 580, 490)
    
    # Información del curso
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 470, "DATOS DEL PROGRAMA DE CAPACITACIÓN:")
    c.setFont("Helvetica", 10)
    
    c.drawString(50, 450, f"Curso: {data.get('nombre_curso', '')}")
    c.drawString(50, 430, f"Horas: {data.get('horas_curso', '')}")
    c.drawString(50, 410, f"Área Temática: {data.get('area_tematica', '')}")
    
    # Fechas
    fecha_inicio = data.get('fecha_inicio', '')
    fecha_fin = data.get('fecha_fin', '')
    c.drawString(50, 390, f"Fecha Inicio: {fecha_inicio}")
    c.drawString(50, 370, f"Fecha Fin: {fecha_fin}")
    
    # Línea separadora
    c.line(30, 350, 580, 350)
    
    # Instructor
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 330, "INSTRUCTOR:")
    c.setFont("Helvetica", 10)
    c.drawString(50, 310, f"{data.get('instructor_nombre', '')}")
    
    # Representantes
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 290, "REPRESENTANTES:")
    c.setFont("Helvetica", 10)
    c.drawString(50, 270, f"Legal: {data.get('representante_legal', '')}")
    c.drawString(50, 250, f"Trabajadores: {data.get('representante_trabajadores', '')}")
    
    # Fecha de emisión
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, 220, f"Fecha de Emisión: {datetime.now().strftime('%d/%m/%Y')}")
    

    
    c.save()
    pdf_buffer.seek(0)
    
    return pdf_buffer.getvalue()

@login_required
def llenar_plantilla_dc3_sistema(request):
    """
    Vista para llenar plantillas DC-3 directamente en el sistema
    """
    if request.method == 'POST':
        form = DC3GenerateForm(request.POST)
        print(f"POST recibido: {request.POST}")
        print(f"Formulario válido: {form.is_valid()}")
        
        if form.is_valid():
            # Obtener datos del formulario
            data = form.cleaned_data
            print(f"Datos limpios: {data}")
            
            # Obtener el ID de la plantilla seleccionada
            plantilla_id = data.get('plantilla')
            print(f"Plantilla seleccionada ID: {plantilla_id}")
            
            # Si no se seleccionó plantilla, usar la del curso pre-cargado
            if not plantilla_id:
                # Obtener la última inscripción del usuario para determinar la organización
                ultima_inscripcion = Inscripcion.objects.filter(alumno=request.user).select_related('curso__organizacion').order_by('-fecha_inscripcion').first()
                if ultima_inscripcion and ultima_inscripcion.curso.organizacion:
                    if ultima_inscripcion.curso.organizacion.nombre == "Fraternidad Migratoria":
                        plantilla_id = 10
                    elif ultima_inscripcion.curso.organizacion.nombre == "CPI":
                        plantilla_id = 11
                    else:
                        plantilla_id = 10  # Fallback
                else:
                    plantilla_id = 10  # Fallback por defecto
            
            # Generar certificado usando caracteres individuales con coordenadas personalizadas
            # Coordenadas para caracteres individuales (las que configuraste)
            coordenadas_caracteres = {
                # CURP (18 caracteres)
                'curp_0': (43, 593), 'curp_1': (58, 593), 'curp_2': (72, 593), 'curp_3': (88, 593),
                'curp_4': (102, 593), 'curp_5': (117, 593), 'curp_6': (132, 593), 'curp_7': (145, 593),
                'curp_8': (158, 593), 'curp_9': (172, 593), 'curp_10': (187, 593), 'curp_11': (201, 593),
                'curp_12': (217, 593), 'curp_13': (233, 593), 'curp_14': (250, 593), 'curp_15': (265, 593),
                'curp_16': (279, 593), 'curp_17': (297, 593),
                
                # RFC (13 caracteres)
                'rfc_0': (45, 496), 'rfc_1': (58, 496), 'rfc_2': (72, 496), 'rfc_3': (90, 496),
                'rfc_4': (118, 496), 'rfc_5': (132, 496), 'rfc_6': (144, 496), 'rfc_7': (157, 496),
                'rfc_8': (172, 496), 'rfc_9': (186, 496), 'rfc_10': (217, 496), 'rfc_11': (233, 496),
                'rfc_12': (250, 496),
                
                # Fecha Inicio (solo las posiciones con coordenadas válidas)
                'fecha_ini_0': (260, 416), 'fecha_ini_1': (277, 416), 'fecha_ini_2': (292, 416),
                'fecha_ini_3': (308, 416), 'fecha_ini_5': (327, 416), 'fecha_ini_6': (347, 416),
                'fecha_ini_8': (368, 416), 'fecha_ini_9': (390, 416),
                
                # Fecha Fin (solo las posiciones con coordenadas válidas)
                'fecha_fin_0': (431, 416), 'fecha_fin_1': (450, 416), 'fecha_fin_2': (470, 416),
                'fecha_fin_3': (487, 416), 'fecha_fin_5': (510, 416), 'fecha_fin_6': (530, 416),
                'fecha_fin_8': (550, 416), 'fecha_fin_9': (570, 416)
            }
            
            # Agregar información del usuario que genera y posible inscripción relacionada
            data['usuario_generador'] = request.user
            
            # Buscar inscripción relacionada con el curso
            inscripcion_relacionada = None
            try:
                inscripciones = Inscripcion.objects.filter(
                    alumno=request.user,
                    curso__nombre__icontains=data.get('nombre_curso', '')
                ).order_by('-fecha_inscripcion')
                
                if inscripciones.exists():
                    inscripcion_relacionada = inscripciones.first()
                    
                    # Verificar si ya existe un certificado para esta inscripción
                    if CertificadoDC3.objects.filter(inscripcion=inscripcion_relacionada).exists():
                        print(f"DEBUG - Ya existe un certificado para esta inscripción: {inscripcion_relacionada.id}")
                        messages.error(request, 'Ya has generado un certificado para este curso. Solo se permite un certificado por inscripción.')
                        return redirect('mis_cursos')
                    
                    data['inscripcion_relacionada'] = inscripcion_relacionada
                    print(f"📝 Inscripción relacionada encontrada: {inscripcion_relacionada}")
                else:
                    print(f"📝 No se encontró inscripción relacionada para el curso: {data.get('nombre_curso', '')}")
            except Exception as e:
                print(f"Error buscando inscripción relacionada: {e}")
            
            pdf_content = generar_pdf_con_caracteres_individuales(data, plantilla_id, coordenadas_caracteres)
            
            # Generar nombre de archivo
            nombre_archivo = f"DC3_{data['apellido_paterno']}_{data['apellido_materno']}_{data['nombres']}_{datetime.now().strftime('%Y%m%d')}.pdf"
            
            # Crear respuesta para descarga
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
            
            print(f"PDF generado: {len(pdf_content)} bytes")
            print(f"Nombre archivo: {nombre_archivo}")
            
            return response
        else:
            print(f"Errores del formulario: {form.errors}")
    else:
        # Prefill with the latest enrolled course for this user
        initial = {}
        try:
            ultima_inscripcion = Inscripcion.objects.filter(alumno=request.user).select_related('curso__organizacion').order_by('-fecha_inscripcion').first()
            if ultima_inscripcion and ultima_inscripcion.curso:
                initial['nombre_curso'] = ultima_inscripcion.curso.nombre
                initial['horas_curso'] = str(ultima_inscripcion.curso.duracion_horas) if ultima_inscripcion.curso.duracion_horas else ''
                
                # Pre-seleccionar la plantilla según la organización del curso
                if ultima_inscripcion.curso.organizacion:
                    if ultima_inscripcion.curso.organizacion.nombre == "Fraternidad Migratoria":
                        initial['plantilla'] = 10
                    elif ultima_inscripcion.curso.organizacion.nombre == "CPI":
                        initial['plantilla'] = 11
                    else:
                        initial['plantilla'] = 10  # Fallback
                else:
                    initial['plantilla'] = 10  # Fallback por defecto
        except Exception as e:
            print(f"DEBUG - No se pudo precargar curso desde inscripciones: {e}")
        form = DC3GenerateForm(initial=initial)
    
    # Obtener plantillas disponibles
    plantillas = PlantillaDC3.objects.filter(activo=True)
    
    # Verificar si el usuario ya tiene certificados generados
    certificados_existentes = []
    if request.user.is_authenticated:
        inscripciones = Inscripcion.objects.filter(alumno=request.user).select_related('curso')
        for inscripcion in inscripciones:
            if CertificadoDC3.objects.filter(inscripcion=inscripcion).exists():
                certificados_existentes.append({
                    'nombre': inscripcion.curso.nombre,
                    'fecha': inscripcion.fecha_inscripcion.strftime('%d/%m/%Y'),
                    'inscripcion_id': inscripcion.id
                })
    
    return render(request, 'cursos/llenar_plantilla_sistema.html', {
        'form': form,
        'plantillas': plantillas,
        'certificados_existentes': certificados_existentes
    })

@login_required
def previsualizar_certificado(request):
    """
    Vista para previsualizar el certificado en tiempo real
    """
    if request.method == 'POST':
        form = DC3GenerateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            return render(request, 'cursos/previsualizar_certificado.html', {
                'data': data,
                'form': form
            })
    
    return redirect('llenar_plantilla_dc3_sistema')

@login_required
def obtener_plantilla_preview(request, plantilla_id):
    """
    Vista para obtener una previsualización de la plantilla seleccionada
    """
    try:
        plantilla = PlantillaDC3.objects.get(id=plantilla_id, activo=True)
        return JsonResponse({
            'success': True,
            'nombre': plantilla.nombre,
            'url': plantilla.archivo.url if plantilla.archivo else None
        })
    except PlantillaDC3.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Plantilla no encontrada'
        })

@login_required
def mapear_coordenadas(request):
    """
    Vista para mostrar el formulario de mapeo de coordenadas
    """
    # Solo permitir acceso a profesores
    if request.user.rol != "profesor":
        return HttpResponse('Acceso denegado. Solo los profesores pueden acceder a esta herramienta.', status=403)
    return render(request, 'cursos/mapear_coordenadas.html')

@login_required
def generar_con_coordenadas(request):
    """
    Vista para generar PDF con coordenadas personalizadas
    """
    # Solo permitir acceso a profesores
    if request.user.rol != "profesor":
        return HttpResponse('Acceso denegado. Solo los profesores pueden acceder a esta herramienta.', status=403)
    
    from datetime import date
    
    if request.method == 'POST':
        # Obtener las coordenadas del formulario
        coordenadas = {}
        campos = [
            'nombres', 'curp', 'puesto', 'nombre_curso', 
            'horas_curso', 'nombre_empresa', 'rfc_empresa',
            'representante_legal', 'representante_trabajadores', 
            'fecha_inicio', 'fecha_fin', 'instructor_nombre'
        ]
        
        for campo in campos:
            x = request.POST.get(f'{campo}_x')
            y = request.POST.get(f'{campo}_y')
            if x and y:
                coordenadas[campo] = (int(x), int(y))
        
        # Datos de prueba
        data = {
            'apellido_paterno': 'AGUILA',
            'apellido_materno': 'MENDIETA', 
            'nombres': 'FERNANDO',
            'curp': 'AUMF970410HDFGNR02',
            'puesto': 'TECNICO',
            'nombre_curso': 'BRIGADA CONTRA INCENDIOS',
            'horas_curso': '4',
            'nombre_empresa': 'ADMINITRACION DE CONDOMINIOS MY HOGAR',
            'rfc_empresa': 'ADMINITRACION',
            'representante_legal': 'MARIA DEL CARMEL GARCIA',
            'representante_trabajadores': 'JUAN CARLOS DE ROSA',
            'fecha_inicio': date(2025, 8, 15),
            'fecha_fin': date(2025, 8, 15),
            'instructor_nombre': 'EDUARDO MENDIETA ZUÑIGA',
        }
        
        try:
            # Generar PDF con coordenadas personalizadas
            pdf_content = generar_pdf_con_plantilla(data, 10, coordenadas)
            
            # Crear respuesta HTTP
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="DC3_coordenadas_personalizadas.pdf"'
            
            return response
            
        except Exception as e:
            print(f"Error al generar PDF con coordenadas personalizadas: {e}")
            return HttpResponse(f"Error: {e}", status=500)
    
    return HttpResponse("Método no permitido", status=405)

@login_required
def mapeo_caracteres_individuales(request):
    """
    Vista para mostrar el formulario de mapeo de caracteres individuales
    """
    # Solo permitir acceso a profesores
    if request.user.rol != "profesor":
        return HttpResponse('Acceso denegado. Solo los profesores pueden acceder a esta herramienta.', status=403)
    return render(request, 'cursos/mapeo_caracteres_individuales.html')

@login_required
def generar_con_caracteres_individuales(request):
    """
    Vista para generar PDF con coordenadas de caracteres individuales
    """
    # Solo permitir acceso a profesores
    if request.user.rol != "profesor":
        return HttpResponse('Acceso denegado. Solo los profesores pueden acceder a esta herramienta.', status=403)
    
    from datetime import date
    
    if request.method == 'POST':
        # Obtener las coordenadas de caracteres individuales
        coordenadas_caracteres = {}

        def add_coord_if_numeric(prefix: str, index: int):
            key_x = f"{prefix}_{index}_x"
            key_y = f"{prefix}_{index}_y"
            x_raw = request.POST.get(key_x, "").strip()
            y_raw = request.POST.get(key_y, "").strip()
            if not x_raw or not y_raw:
                return
            try:
                x_val = int(x_raw)
                y_val = int(y_raw)
            except (TypeError, ValueError):
                # Ignorar valores no numéricos como "X" o "Y"
                return
            coordenadas_caracteres[f'{prefix}_{index}'] = (x_val, y_val)

        # CURP - 18 caracteres
        for i in range(18):
            add_coord_if_numeric('curp', i)

        # RFC - 13 caracteres
        for i in range(13):
            add_coord_if_numeric('rfc', i)

        # Fecha Inicio - 10 caracteres (índices 0..9)
        for i in range(10):
            add_coord_if_numeric('fecha_ini', i)

        # Fecha Fin - 10 caracteres (índices 0..9)
        for i in range(10):
            add_coord_if_numeric('fecha_fin', i)
        
        # Datos de prueba
        data = {
            'apellido_paterno': 'AGUILA',
            'apellido_materno': 'MENDIETA', 
            'nombres': 'FERNANDO',
            'curp': 'AUMF970410HDFGNR02',
            'puesto': 'TECNICO',
            'nombre_curso': 'BRIGADA CONTRA INCENDIOS',
            'horas_curso': '4',
            'nombre_empresa': 'ADMINITRACION DE CONDOMINIOS MY HOGAR',
            'rfc_empresa': 'ADMINITRACION',
            'representante_legal': 'MARIA DEL CARMEL GARCIA',
            'representante_trabajadores': 'JUAN CARLOS DE ROSA',
            'fecha_inicio': date(2025, 8, 16),
            'fecha_fin': date(2025, 8, 16),
            'instructor_nombre': 'EDUARDO MENDIETA ZUÑIGA',
        }
        
        try:
            # Generar PDF con caracteres individuales
            pdf_content = generar_pdf_con_caracteres_individuales(data, 10, coordenadas_caracteres)
            
            # Crear respuesta HTTP
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="DC3_caracteres_individuales.pdf"'
            
            return response
            
        except Exception as e:
            print(f"Error al generar PDF con caracteres individuales: {e}")
            return HttpResponse(f"Error: {e}", status=500)
    
    return HttpResponse("Método no permitido", status=405)

def proteger_pdf_con_contraseña(output):
    """
    Función auxiliar para proteger un PDF con restricciones de solo lectura
    """
    # Configurar restricciones de seguridad sin contraseña de apertura
    output.encrypt('', '', 
                  use_128bit=True,
                  permissions_flag=0)  # 0 = solo lectura
    
    return output

def agregar_proteccion_avanzada(canvas, data):
    """
    Agrega protección avanzada al PDF con sistema de verificación simple y efectivo
    """
    from reportlab.lib.colors import Color
    from hashlib import sha256
    import json
    
    # Crear código de verificación único basado en los datos
    datos_verificacion = {
        'curp': data.get('curp', ''),
        'curso': data.get('nombre_curso', ''),
        'fecha': str(data.get('fecha_inicio', '')),
        'institucion': 'ICCSI'
    }
    
    # Crear hash único
    datos_string = json.dumps(datos_verificacion, sort_keys=True)
    hash_verificacion = sha256(datos_string.encode()).hexdigest()
    codigo_verificacion = hash_verificacion[:12].upper()
    
    # Agregar marcas de agua visibles pero discretas
    color_discreto = Color(0.8, 0.8, 0.8, alpha=0.3)  # Gris claro semi-transparente
    canvas.setFillColor(color_discreto)
    canvas.setFont("Helvetica", 4)
    
    # Agregar marcas de agua en las esquinas
    marcas = [
        f"ICCSI_{codigo_verificacion}",
        f"VERIFY_{hash_verificacion[:8]}",
        f"OFFICIAL_{data.get('curp', '')[:8]}",
        f"SECURE_{data.get('fecha_inicio', '')}"
    ]
    
    posiciones = [(50, 50), (550, 50), (50, 750), (550, 750)]
    for i, (x, y) in enumerate(posiciones):
        if i < len(marcas):
            canvas.drawString(x, y, marcas[i])
    
    # Restaurar color
    canvas.setFillColor(Color(0, 0, 0, alpha=1))

def generar_folio_unico(data):
    """
    Genera un folio único para el certificado DC-3
    Formato: DC3-YYYY-XXXXX (año + número secuencial)
    """
    from datetime import datetime
    from .models import HistorialCertificadoDC3
    
    año_actual = datetime.now().year
    
    # Buscar el último folio del año actual
    ultimo_folio = HistorialCertificadoDC3.objects.filter(
        folio__startswith=f'DC3-{año_actual}-'
    ).order_by('-folio').first()
    
    if ultimo_folio and ultimo_folio.folio:
        # Extraer el número del último folio
        try:
            ultimo_numero = int(ultimo_folio.folio.split('-')[-1])
            nuevo_numero = ultimo_numero + 1
        except (ValueError, IndexError):
            nuevo_numero = 1
    else:
        nuevo_numero = 1
    
    # Formatear el folio: DC3-2025-00001
    folio = f'DC3-{año_actual}-{nuevo_numero:05d}'
    
    return folio

def generar_codigo_verificacion_unico(data):
    """
    Genera un código de verificación único basado en los datos del certificado
    """
    from hashlib import sha256
    import json
    import secrets
    import string
    
    # Crear código basado en datos únicos
    datos_verificacion = {
        'curp': data.get('curp', ''),
        'fecha': str(data.get('fecha_inicio', '')),
        'curso': data.get('nombre_curso', '')[:20],
        'empresa': data.get('nombre_empresa', '')[:20],
        'nombres': data.get('nombres', ''),
        'timestamp': str(datetime.now().timestamp()),
        'random': secrets.token_hex(4)  # Agregar aleatoriedad
    }
    
    # Generar código único de 8 caracteres (más fácil de leer)
    codigo_base = sha256(json.dumps(datos_verificacion, sort_keys=True).encode()).hexdigest()[:8].upper()
    
    # Asegurar que el código sea único en la base de datos
    from .models import HistorialCertificadoDC3
    codigo_verificacion = codigo_base
    contador = 1
    
    while HistorialCertificadoDC3.objects.filter(codigo_verificacion=codigo_verificacion).exists():
        # Si existe, agregar un sufijo
        codigo_verificacion = f"{codigo_base[:-2]}{contador:02d}"
        contador += 1
        if contador > 99:
            # Si llegamos a 99, generar uno completamente nuevo
            codigo_verificacion = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    
    return codigo_verificacion


def agregar_texto_verificacion_simple(canvas, data):
    """
    Agrega texto de verificación con folio y código de autenticación visible
    """
    from reportlab.lib.colors import Color
    
    # Obtener folio y código de verificación
    folio = data.get('folio', generar_folio_unico(data))
    codigo_verificacion = data.get('codigo_verificacion', generar_codigo_verificacion_unico(data))
    
    # Configurar color negro sólido
    canvas.setFillColor(Color(0, 0, 0, alpha=1.0))
    
    # Agregar folio en la esquina superior derecha
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawString(470, 770, f"FOLIO: {folio}")
    
    # Agregar código de autenticación visible en el centro superior
    canvas.setFont("Helvetica-Bold", 12)
    canvas.drawString(200, 750, codigo_verificacion)
    
    # Agregar folio en la parte inferior izquierda
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(10, 90, f"FOLIO: {folio}")
    
    # Agregar código de autenticación en la parte inferior derecha
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawString(400, 90, codigo_verificacion)
    
    # Restaurar color
    canvas.setFillColor(Color(0, 0, 0, alpha=1))


def guardar_en_historial_certificado(data, codigo_verificacion, folio, archivo_pdf_path=None, usuario=None, inscripcion=None):
    """
    Guarda el certificado generado en el historial para verificación posterior
    """
    from .models import HistorialCertificadoDC3
    
    # Crear nombre completo del alumno
    nombre_completo = f"{data.get('apellido_paterno', '')} {data.get('apellido_materno', '')} {data.get('nombres', '')}".strip()
    
    # Crear registro en el historial
    historial = HistorialCertificadoDC3.objects.create(
        nombre_completo_alumno=nombre_completo,
        apellido_paterno=data.get('apellido_paterno', ''),
        apellido_materno=data.get('apellido_materno', ''),
        nombres=data.get('nombres', ''),
        curp=data.get('curp', ''),
        nombre_empresa=data.get('nombre_empresa', ''),
        rfc_empresa=data.get('rfc_empresa', ''),
        nombre_curso=data.get('nombre_curso', ''),
        horas_curso=int(data.get('horas_curso', 0)),
        fecha_inicio=data.get('fecha_inicio'),
        fecha_fin=data.get('fecha_fin'),
        instructor_nombre=data.get('instructor_nombre', ''),
        folio=folio,
        codigo_verificacion=codigo_verificacion,
        archivo_pdf_path=archivo_pdf_path,
        inscripcion=inscripcion,
        generado_por=usuario
    )
    
    print(f"📝 Certificado guardado en historial: {historial.codigo_verificacion}")
    return historial



def extraer_datos_pdf(pdf_content):
    """
    Extrae el folio y código de autenticación del PDF para verificación
    """
    from PyPDF2 import PdfReader
    import re
    import io
    
    try:
        # Leer el PDF
        pdf_reader = PdfReader(io.BytesIO(pdf_content))
        content_data = b''
        
        # Extraer contenido de todas las páginas
        for page in pdf_reader.pages:
            if '/Contents' in page:
                contents = page['/Contents']
                if hasattr(contents, 'get_data'):
                    content_data += contents.get_data()
        
        # Convertir a string para búsqueda
        content_str = content_data.decode('utf-8', errors='ignore')
        
        datos_extraidos = {
            'folio': None,
            'codigo_autenticacion': None
        }
        
        # Buscar folio
        patrones_folio = [
            r'FOLIO:\s*(DC3-\d{4}-\d{5})',
            r'(DC3-\d{4}-\d{5})',
        ]
        
        # Buscar código de autenticación
        patrones_codigo = [
            r'([A-F0-9]{8})',               # Solo el código de 8 caracteres
        ]
        
        # Buscar folio
        for patron in patrones_folio:
            matches = re.findall(patron, content_str)
            if matches:
                datos_extraidos['folio'] = matches[0]
                break
        
        # Buscar código de autenticación
        for patron in patrones_codigo:
            matches = re.findall(patron, content_str)
            if matches:
                datos_extraidos['codigo_autenticacion'] = matches[0]
                break
        
        return datos_extraidos
        
    except Exception as e:
        print(f"Error extrayendo datos del PDF: {e}")
        return {
            'folio': None,
            'codigo_autenticacion': None
        }


def verificar_autenticidad_pdf(pdf_content):
    """
    Verifica la autenticidad de un PDF certificado DC-3 usando múltiples criterios
    """
    from PyPDF2 import PdfReader
    from hashlib import sha256, md5
    from .models import HistorialCertificadoDC3, Inscripcion
    import json
    import io
    from datetime import datetime, timedelta
    
    try:
        # Extraer folio y código de autenticación del PDF
        datos_extraidos = extraer_datos_pdf(pdf_content)
        folio = datos_extraidos['folio']
        codigo_autenticacion = datos_extraidos['codigo_autenticacion']
        
        # Buscar en TODA la base de datos usando múltiples criterios
        certificado_bd = None
        inscripcion_valida = None
        tipo_busqueda = "Búsqueda completa en base de datos"
        coincidencias_encontradas = []
        total_certificados_revisados = 0
        
        # 1. Primero intentar búsqueda por código de autenticación (más específica)
        if codigo_autenticacion:
            try:
                certificado_bd = HistorialCertificadoDC3.objects.get(codigo_verificacion=codigo_autenticacion)
                tipo_busqueda = "Búsqueda por Código de Autenticación"
                coincidencias_encontradas.append(f"Código: {codigo_autenticacion}")
                total_certificados_revisados = 1
            except HistorialCertificadoDC3.DoesNotExist:
                pass
        
        # 2. Si no se encontró por código, intentar por folio
        if not certificado_bd and folio:
            try:
                certificado_bd = HistorialCertificadoDC3.objects.get(folio=folio)
                tipo_busqueda = "Búsqueda por Folio Exacto"
                coincidencias_encontradas.append(f"Folio: {folio}")
                total_certificados_revisados = 1
            except HistorialCertificadoDC3.DoesNotExist:
                pass
        
        # 3. Si no se encontró por código ni folio, NO buscar por otros criterios
        # Esto evita falsos positivos. Solo certificados con código o folio válidos son auténticos
        if not certificado_bd:
            tipo_busqueda = "No encontrado - Código y folio no válidos"
            total_certificados_revisados = 0
        
        # Verificar inscripción válida si se encontró certificado
        if certificado_bd:
            if certificado_bd.inscripcion:
                inscripcion_valida = certificado_bd.inscripcion
            else:
                # Buscar inscripción por datos del alumno y curso
                inscripciones = Inscripcion.objects.filter(
                    alumno__first_name__icontains=certificado_bd.nombres,
                    curso__nombre__icontains=certificado_bd.nombre_curso
                )
                if inscripciones.exists():
                    inscripcion_valida = inscripciones.first()
        
        # Verificar autenticidad basada en la base de datos
        es_autentico = bool(certificado_bd)
        
        # Nivel de autenticidad (máximo 10)
        nivel_autenticidad = 10 if es_autentico else 0
        
        # Verificar hash de integridad
        hash_actual = sha256(pdf_content).hexdigest()
        hash_md5 = md5(pdf_content).hexdigest()
        
        resultado = {
            'autentico': es_autentico,
            'nivel_autenticidad': nivel_autenticidad,
            'max_nivel': 10,
            'folio': folio,
            'codigo_autenticacion': codigo_autenticacion,
            'encontrado_en_bd': bool(certificado_bd),
            'inscripcion_valida': bool(inscripcion_valida),
            'hash_sha256': hash_actual,
            'hash_md5': hash_md5,
            'tamano_bytes': len(pdf_content),
            'institucion': 'ICCSI',
            'fecha_verificacion': str(timezone.now()),
            'version_proteccion': '6.0 - Sistema con Código de Autenticación',
            'tipo_busqueda': tipo_busqueda,
            'total_certificados_revisados': total_certificados_revisados,
            'coincidencias_encontradas': coincidencias_encontradas,
            'datos_extraidos_pdf': {
                'folio': folio,
                'codigo_autenticacion': codigo_autenticacion
            }
        }
        
        # Agregar datos del certificado si se encontró
        if certificado_bd:
            resultado.update({
                'datos_alumno': {
                    'nombre_completo': certificado_bd.nombre_completo_alumno,
                    'curp': certificado_bd.curp
                },
                'datos_empresa': {
                    'nombre': certificado_bd.nombre_empresa,
                    'rfc': certificado_bd.rfc_empresa
                },
                'datos_curso': {
                    'nombre': certificado_bd.nombre_curso,
                    'horas': certificado_bd.horas_curso,
                    'instructor': certificado_bd.instructor_nombre,
                    'fecha_inicio': certificado_bd.fecha_inicio.strftime('%d/%m/%Y'),
                    'fecha_fin': certificado_bd.fecha_fin.strftime('%d/%m/%Y')
                },
                'fecha_generacion': certificado_bd.fecha_generacion.strftime('%d/%m/%Y %H:%M'),
                'generado_por': certificado_bd.generado_por.username if certificado_bd.generado_por else 'Sistema',
                'total_certificados_encontrados': 1,
                'folio_real': certificado_bd.folio,
                'codigo_verificacion': certificado_bd.codigo_verificacion
            })
        
        return resultado
        
    except Exception as e:
        print(f"Error verificando autenticidad: {e}")
        from django.utils import timezone
        return {
            'autentico': False,
            'error': str(e),
            'nivel_autenticidad': 0,
            'max_nivel': 10,
            'folio': None,
            'encontrado_en_bd': False,
            'inscripcion_valida': False,
            'institucion': 'ICCSI',
            'fecha_verificacion': str(timezone.now()),
            'version_proteccion': '6.0 - Sistema con Código de Autenticación',
            'tipo_busqueda': 'Error en verificación'
        }

def generar_pdf_con_caracteres_individuales(data, plantilla_id, coordenadas_caracteres):
    """
    Genera un PDF usando la plantilla PDF con caracteres individuales posicionados
    """
    from PyPDF2 import PdfReader, PdfWriter
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.colors import black
    import io
    from datetime import datetime
    
    # Obtener la plantilla
    plantilla = PlantillaDC3.objects.get(id=plantilla_id, activo=True)
    
    # Leer la plantilla PDF
    with open(plantilla.archivo.path, 'rb') as template_file:
        template_reader = PdfReader(template_file)
        template_page = template_reader.pages[0]
        
        # Crear un nuevo PDF con los datos
        output = PdfWriter()
        
        # Crear un PDF temporal con los datos del formulario
        data_pdf = io.BytesIO()
        c = canvas.Canvas(data_pdf)
        
        # Configurar fuente y tamaño
        c.setFont("Helvetica", 10)
        
        # Coordenadas para campos normales (no caracteres individuales)
        posiciones_normales = {
            'nombres': (225, 620),           # Nombre completo
            'apellido_paterno': (225, 620),  # Apellido paterno (mismo que nombres)
            'apellido_materno': (225, 620),  # Apellido materno (mismo que nombres)
            'puesto': (77, 578),             # Puesto
            'nombre_curso': (114, 450),      # Nombre del curso (coordenadas actualizadas)
            'horas_curso': (54, 416),        # Horas del curso
            'nombre_empresa': (200, 525),    # Nombre de la empresa
            'representante_legal': (225, 302), # Representante legal
            'representante_trabajadores': (400, 302), # Representante trabajadores
            'instructor_nombre': (50, 302),  # Instructor
        }
        
        # Escribir campos normales
        for campo, (x, y) in posiciones_normales.items():
            if campo in ['nombres', 'apellido_paterno', 'apellido_materno']:
                # Combinar nombre completo: APELLIDOS + NOMBRES
                apellido_paterno = data.get('apellido_paterno', '')
                apellido_materno = data.get('apellido_materno', '')
                nombres = data.get('nombres', '')
                nombre_completo = f"{apellido_paterno} {apellido_materno} {nombres}".strip()
                if campo == 'nombres':  # Solo escribir una vez
                    c.drawString(x, y, nombre_completo)
                continue
            elif campo in ['apellido_paterno', 'apellido_materno']:
                continue  # Ya se manejó arriba
            elif campo == 'nombre_curso':
                # Manejar texto largo del curso con múltiples líneas
                valor = data.get(campo, '')
                print(f"DEBUG - Escribiendo campo '{campo}': '{valor}' en coordenadas ({x}, {y})")
                
                # Configuración para el recuadro del curso
                ancho_maximo = 490  # Ancho máximo del recuadro (optimizado)
                alto_linea = 11     # Altura entre líneas (optimizada)
                fuente_base = 8     # Tamaño de fuente base (reducido)
                
                # Dividir el texto en palabras
                palabras = valor.split()
                lineas = []
                linea_actual = ""
                
                for palabra in palabras:
                    # Probar si la palabra cabe en la línea actual
                    texto_prueba = linea_actual + " " + palabra if linea_actual else palabra
                    c.setFont("Helvetica", fuente_base)
                    ancho_texto = c.stringWidth(texto_prueba, "Helvetica", fuente_base)
                    
                    if ancho_texto <= ancho_maximo:
                        linea_actual = texto_prueba
                    else:
                        if linea_actual:
                            lineas.append(linea_actual)
                        linea_actual = palabra
                
                # Agregar la última línea
                if linea_actual:
                    lineas.append(linea_actual)
                
                # Si no hay líneas, usar el texto original
                if not lineas:
                    lineas = [valor]
                
                # Escribir cada línea
                for i, linea in enumerate(lineas):
                    y_linea = y - (i * alto_linea)
                    c.setFont("Helvetica", fuente_base)
                    c.drawString(x, y_linea, linea)
                
                # Restablecer la fuente a la predeterminada
                c.setFont("Helvetica", 10)
            else:
                valor = data.get(campo, '')
                if hasattr(valor, 'strftime'):  # Verificar si es una fecha
                    valor = valor.strftime('%d/%m/%Y')
                print(f"DEBUG - Escribiendo campo '{campo}': '{valor}' en coordenadas ({x}, {y})")
                c.drawString(x, y, str(valor))
        
        # Escribir CURP carácter por carácter
        curp = str(data.get('curp', '')).upper()
        for i, char in enumerate(curp):
            if i < 18 and f'curp_{i}' in coordenadas_caracteres:
                x, y = coordenadas_caracteres[f'curp_{i}']
                c.drawString(x, y, char)
        
        # Escribir RFC carácter por carácter
        rfc = str(data.get('rfc_empresa', '')).upper()
        for i, char in enumerate(rfc):
            if i < 13 and f'rfc_{i}' in coordenadas_caracteres:
                x, y = coordenadas_caracteres[f'rfc_{i}']
                c.drawString(x, y, char)
        
        # Escribir Fecha Inicio carácter por carácter (formato YYYYMMDD sin barras)
        if hasattr(data.get('fecha_inicio'), 'strftime'):
            fecha_ini_str = data.get('fecha_inicio').strftime('%Y%m%d')
        else:
            fecha_ini_str = str(data.get('fecha_inicio', '')).replace('/', '')

        # Mapear los 10 índices de la UI (0..9) a 8 caracteres reales sin barras.
        # Dejamos hueco en 4 y 7 (donde antes iban las '/') para respetar tus coordenadas.
        # Indices reales: 0 1 2 3 4 5 6 7  (8 chars)
        # Indices UI:     0 1 2 3 4 5 6 7 8 9 (10)
        mapping_ini = {
            0: 0,  # 2
            1: 1,  # 0
            2: 2,  # 2
            3: 3,  # 5
            # 4: separador omitido (era /)
            5: 4,  # 0
            6: 5,  # 8
            # 7: separador omitido (era /)
            8: 6,  # 1
            9: 7,  # 6
        }
        for ui_index in range(10):
            if f'fecha_ini_{ui_index}' not in coordenadas_caracteres:
                continue
            if ui_index not in mapping_ini:
                # Hueco (antes era '/')
                continue
            real_index = mapping_ini[ui_index]
            if real_index < len(fecha_ini_str):
                x, y = coordenadas_caracteres[f'fecha_ini_{ui_index}']
                c.drawString(x, y, fecha_ini_str[real_index])

        # Escribir Fecha Fin carácter por carácter (formato YYYYMMDD sin barras)
        if hasattr(data.get('fecha_fin'), 'strftime'):
            fecha_fin_str = data.get('fecha_fin').strftime('%Y%m%d')
        else:
            fecha_fin_str = str(data.get('fecha_fin', '')).replace('/', '')

        mapping_fin = mapping_ini
        for ui_index in range(10):
            if f'fecha_fin_{ui_index}' not in coordenadas_caracteres:
                continue
            if ui_index not in mapping_fin:
                continue
            real_index = mapping_fin[ui_index]
            if real_index < len(fecha_fin_str):
                x, y = coordenadas_caracteres[f'fecha_fin_{ui_index}']
                c.drawString(x, y, fecha_fin_str[real_index])
        
        # Generar código de verificación único
        codigo_verificacion = generar_codigo_verificacion_unico(data)
        data['codigo_verificacion'] = codigo_verificacion
        
        # Generar folio único ANTES de agregar el texto
        folio = generar_folio_unico(data)
        data['folio'] = folio
        
        # Agregar protección avanzada con múltiples capas
        agregar_proteccion_avanzada(c, data)
        
        # Agregar texto de verificación avanzado
        agregar_texto_verificacion_simple(c, data)
        
        c.save()
        data_pdf.seek(0)
        
        # Combinar la plantilla con los datos
        data_reader = PdfReader(data_pdf)
        data_page = data_reader.pages[0]
        
        # Superponer los datos sobre la plantilla
        template_page.merge_page(data_page)
        output.add_page(template_page)
        
        # Proteger el PDF con contraseña
        # output = proteger_pdf_con_contraseña(output)  # DESHABILITADO para permitir extracción de texto
        
        # Generar el PDF final
        result_pdf = io.BytesIO()
        output.write(result_pdf)
        result_pdf.seek(0)
        
        # Guardar en historial para verificación
        pdf_content = result_pdf.getvalue()
        archivo_nombre = f"DC3_{data.get('apellido_paterno', '')}_{data.get('apellido_materno', '')}_{data.get('nombres', '')}_{timezone.now().strftime('%Y%m%d')}.pdf"
        
        # Guardar registro en historial
        print(f"🔍 DEBUG - Guardando certificado:")
        print(f"   Folio: {folio}")
        print(f"   Código: {codigo_verificacion}")
        print(f"   Alumno: {data.get('apellido_paterno', '')} {data.get('apellido_materno', '')} {data.get('nombres', '')}")
        
        try:
            historial = guardar_en_historial_certificado(
                data=data, 
                codigo_verificacion=codigo_verificacion,
                folio=folio,
                archivo_pdf_path=archivo_nombre,
                usuario=getattr(data, 'usuario_generador', None),
                inscripcion=getattr(data, 'inscripcion_relacionada', None)
            )
            print(f"✅ Certificado guardado exitosamente: {historial.folio}")
        except Exception as e:
            print(f"❌ Error guardando certificado: {e}")
            import traceback
            traceback.print_exc()
        
        return pdf_content

@login_required
def descargar_certificado_inscripcion(request, inscripcion_id):
    """
    Vista para descargar el certificado DC-3 generado automáticamente al inscribirse
    """
    inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id, alumno=request.user)
    
    # Verificar si existe un certificado
    if not hasattr(inscripcion, 'certificado') or not inscripcion.certificado.archivo_pdf:
        return HttpResponse('Certificado no encontrado', status=404)
    
    # Servir el archivo PDF
    response = HttpResponse(inscripcion.certificado.archivo_pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{inscripcion.certificado.archivo_pdf.name.split("/")[-1]}"'
    
    return response

def verificar_certificado(request):
    """
    Vista para verificar la autenticidad de un certificado DC-3
    """
    resultado = None
    archivo_subido = False  # Ya no se usan archivos
    busqueda_realizada = False
    
    if request.method == 'POST':
        # Verificar si es búsqueda por código de autenticación
        if 'codigo_autenticacion' in request.POST:
            codigo = request.POST.get('codigo_autenticacion', '').strip().upper()
            busqueda_realizada = True
            
            if codigo:
                # Verificar por código de autenticación
                resultado = verificar_por_codigo_autenticacion(codigo)
            else:
                resultado = {
                    'autentico': False,
                    'error': 'Debe proporcionar un código de autenticación válido'
                }
        else:
            # Si no se proporcionó código, mostrar error
            resultado = {
                'autentico': False,
                'error': 'Debe proporcionar un código de autenticación válido'
            }
            busqueda_realizada = True
    
    return render(request, 'cursos/verificar_certificado.html', {
        'resultado': resultado,
        'archivo_subido': archivo_subido,
        'busqueda_realizada': busqueda_realizada
    })


def verificar_por_codigo_autenticacion(codigo):
    """
    Verifica la autenticidad de un certificado por su código de autenticación
    """
    from .models import HistorialCertificadoDC3
    
    try:
        certificado = HistorialCertificadoDC3.objects.get(codigo_verificacion=codigo)
        
        return {
            'autentico': True,
            'nivel_autenticidad': 10,
            'max_nivel': 10,
            'codigo_autenticacion': codigo,
            'folio': certificado.folio,
            'encontrado_en_bd': True,
            'institucion': 'ICCSI',
            'fecha_verificacion': str(timezone.now()),
            'version_proteccion': '6.0 - Sistema con Código de Autenticación',
            'tipo_busqueda': 'Búsqueda por Código de Autenticación',
            'datos_alumno': {
                'nombre_completo': certificado.nombre_completo_alumno,
                'curp': certificado.curp
            },
            'datos_empresa': {
                'nombre': certificado.nombre_empresa,
                'rfc': certificado.rfc_empresa
            },
            'datos_curso': {
                'nombre': certificado.nombre_curso,
                'horas': certificado.horas_curso,
                'instructor': certificado.instructor_nombre,
                'fecha_inicio': certificado.fecha_inicio.strftime('%d/%m/%Y'),
                'fecha_fin': certificado.fecha_fin.strftime('%d/%m/%Y')
            },
            'fecha_generacion': certificado.fecha_generacion.strftime('%d/%m/%Y %H:%M'),
            'generado_por': certificado.generado_por.username if certificado.generado_por else 'Sistema'
        }
        
    except HistorialCertificadoDC3.DoesNotExist:
        return {
            'autentico': False,
            'nivel_autenticidad': 0,
            'max_nivel': 10,
            'codigo_autenticacion': codigo,
            'error': f'Código de autenticación "{codigo}" no encontrado en la base de datos',
            'institucion': 'ICCSI',
            'fecha_verificacion': str(timezone.now()),
            'version_proteccion': '6.0 - Sistema con Código de Autenticación',
            'tipo_busqueda': 'Búsqueda por Código de Autenticación'
        }


def buscar_certificado_por_nombre_empresa_curso(nombre_alumno, nombre_empresa, nombre_curso=''):
    """
    Busca un certificado en la base de datos por nombre del alumno, empresa y curso
    """
    from .models import HistorialCertificadoDC3
    
    try:
        # Construir filtro base
        filtro_base = {
            'nombre_completo_alumno__icontains': nombre_alumno,
            'nombre_empresa__icontains': nombre_empresa
        }
        
        # Agregar filtro de curso si se proporciona
        if nombre_curso:
            filtro_base['nombre_curso__icontains'] = nombre_curso
        
        # Buscar certificados que coincidan
        certificados = HistorialCertificadoDC3.objects.filter(**filtro_base).order_by('-fecha_generacion')
        
        if certificados.exists():
            # Tomar el más reciente
            certificado = certificados.first()
            
            # Verificar si existe inscripción relacionada
            inscripcion_valida = bool(certificado.inscripcion)
            
            # Determinar tipo de búsqueda para mostrar en resultados
            tipo_busqueda = 'Búsqueda por nombre y empresa'
            if nombre_curso:
                tipo_busqueda = 'Búsqueda por nombre, empresa y curso'
            
            resultado = {
                'autentico': True,
                'nivel_autenticidad': 8,  # Base de datos válida
                'max_nivel': 10,
                'codigo_verificacion': certificado.codigo_verificacion,
                'encontrado_en_bd': True,
                'inscripcion_valida': inscripcion_valida,
                'marcas_agua_encontradas': ['Certificado encontrado en base de datos por búsqueda directa'],
                'patrones_encontrados': [tipo_busqueda],
                'hash_sha256': 'N/A - Búsqueda directa',
                'hash_md5': 'N/A - Búsqueda directa',
                'tamano_bytes': 0,
                'institucion': 'ICCSI',
                'fecha_verificacion': str(datetime.now()),
                'version_proteccion': '3.0',
                'datos_alumno': {
                    'nombre_completo': certificado.nombre_completo_alumno,
                    'nombres': certificado.nombres,
                    'apellido_paterno': certificado.apellido_paterno,
                    'apellido_materno': certificado.apellido_materno,
                    'curp': certificado.curp,
                },
                'datos_empresa': {
                    'nombre': certificado.nombre_empresa,
                    'rfc': certificado.rfc_empresa,
                },
                'datos_curso': {
                    'nombre': certificado.nombre_curso,
                    'horas': certificado.horas_curso,
                    'fecha_inicio': str(certificado.fecha_inicio),
                    'fecha_fin': str(certificado.fecha_fin),
                    'instructor': certificado.instructor_nombre,
                },
                'fecha_generacion': str(certificado.fecha_generacion),
                'generado_por': certificado.generado_por.username if certificado.generado_por else 'Sistema',
                'total_certificados_encontrados': certificados.count(),
                'busqueda_directa': True,
                'criterios_busqueda': {
                    'alumno': nombre_alumno,
                    'empresa': nombre_empresa,
                    'curso': nombre_curso if nombre_curso else 'No especificado'
                }
            }
            
            return resultado
        else:
            # Construir mensaje de error según los criterios de búsqueda
            if nombre_curso:
                error_msg = f'No se encontraron certificados para el alumno "{nombre_alumno}" en la empresa "{nombre_empresa}" con el curso "{nombre_curso}"'
            else:
                error_msg = f'No se encontraron certificados para el alumno "{nombre_alumno}" en la empresa "{nombre_empresa}"'
            
            return {
                'autentico': False,
                'nivel_autenticidad': 0,
                'max_nivel': 10,
                'error': error_msg,
                'institucion': 'ICCSI',
                'fecha_verificacion': str(timezone.now()),
                'version_proteccion': '3.0',
                'busqueda_directa': True,
                'criterios_busqueda': {
                    'alumno': nombre_alumno,
                    'empresa': nombre_empresa,
                    'curso': nombre_curso if nombre_curso else 'No especificado'
                }
            }
            
    except Exception as e:
        return {
            'autentico': False,
            'error': f'Error en la búsqueda: {str(e)}',
            'institucion': 'ICCSI',
            'fecha_verificacion': str(timezone.now()),
            'version_proteccion': '3.0',
            'busqueda_directa': True
        }

@login_required
def mapeo_curso(request):
    """
    Vista para mostrar el formulario de mapeo específico del nombre del curso
    """
    # Solo permitir acceso a profesores
    if request.user.rol != "profesor":
        return HttpResponse('Acceso denegado. Solo los profesores pueden acceder a esta herramienta.', status=403)
    return render(request, 'cursos/mapeo_curso.html')

@login_required
def mapeo_folio(request):
    """
    Vista para mostrar el formulario de mapeo específico del folio
    """
    # Solo permitir acceso a profesores
    if request.user.rol != "profesor":
        return HttpResponse('Acceso denegado. Solo los profesores pueden acceder a esta herramienta.', status=403)
    return render(request, 'cursos/mapeo_folio.html')

@login_required
def generar_con_mapeo_curso(request):
    """
    Vista para generar PDF con coordenadas personalizadas del nombre del curso
    """
    # Solo permitir acceso a profesores
    if request.user.rol != "profesor":
        return HttpResponse('Acceso denegado. Solo los profesores pueden acceder a esta herramienta.', status=403)
    
    from datetime import date
    
    if request.method == 'POST':
        # Obtener las coordenadas del nombre del curso
        x_curso = request.POST.get('nombre_curso_x')
        y_curso = request.POST.get('nombre_curso_y')
        ancho_maximo = request.POST.get('ancho_maximo', '490')
        alto_linea = request.POST.get('alto_linea', '11')
        fuente_base = request.POST.get('fuente_base', '8')
        
        if x_curso and y_curso:
            try:
                coordenadas_curso = {
                    'x': int(x_curso),
                    'y': int(y_curso),
                    'ancho_maximo': int(ancho_maximo),
                    'alto_linea': int(alto_linea),
                    'fuente_base': int(fuente_base)
                }
            except ValueError:
                return HttpResponse("Error: Las coordenadas deben ser números válidos", status=400)
        else:
            return HttpResponse("Error: Se requieren coordenadas X e Y", status=400)
        
        # Datos de prueba con texto largo
        data = {
            'apellido_paterno': 'AGUILA',
            'apellido_materno': 'MENDIETA', 
            'nombres': 'FERNANDO',
            'curp': 'AUMF970410HDFGNR02',
            'puesto': 'TECNICO',
            'nombre_curso': 'NORMA OFICIAL MEXICANA NOM-002-STPS-2010,CONDICIONES DE SEGURIDAD,PREVENCION Y PROTECCION CONTRA INCENDIOS EN LOS CENTROS DE TRABAJO BLOQUEO CANDADEO Y ETIQUETADO (LOTO)',
            'horas_curso': '8',
            'nombre_empresa': 'ADMINITRACION DE CONDOMINIOS MY HOGAR',
            'rfc_empresa': 'ADMINITRACION',
            'representante_legal': 'MARIA DEL CARMEL GARCIA',
            'representante_trabajadores': 'JUAN CARLOS DE ROSA',
            'fecha_inicio': date(2025, 8, 18),
            'fecha_fin': date(2025, 8, 18),
            'instructor_nombre': 'EDUARDO MENDIETA ZUÑIGA',
        }
        
        try:
            # Generar PDF con coordenadas personalizadas del curso
            pdf_content = generar_pdf_con_mapeo_curso(data, 10, coordenadas_curso)
            
            # Crear respuesta HTTP
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="DC3_mapeo_curso.pdf"'
            
            return response
            
        except Exception as e:
            print(f"Error al generar PDF con mapeo de curso: {e}")
            return HttpResponse(f"Error: {e}", status=500)
    
    return HttpResponse("Método no permitido", status=405)

@login_required
def generar_con_mapeo_folio(request):
    """
    Vista para generar PDF con coordenadas personalizadas del folio
    """
    # Solo permitir acceso a profesores
    if request.user.rol != "profesor":
        return HttpResponse('Acceso denegado. Solo los profesores pueden acceder a esta herramienta.', status=403)
    
    from datetime import date
    
    if request.method == 'POST':
        # Obtener las coordenadas del folio
        x_superior = request.POST.get('x_superior')
        y_superior = request.POST.get('y_superior')
        x_inferior = request.POST.get('x_inferior')
        y_inferior = request.POST.get('y_inferior')
        tamano_fuente_superior = request.POST.get('tamano_fuente_superior', '16')
        tamano_fuente_inferior = request.POST.get('tamano_fuente_inferior', '14')
        
        if x_superior and y_superior and x_inferior and y_inferior:
            try:
                coordenadas_folio = {
                    'x_superior': int(x_superior),
                    'y_superior': int(y_superior),
                    'x_inferior': int(x_inferior),
                    'y_inferior': int(y_inferior),
                    'tamano_fuente_superior': int(tamano_fuente_superior),
                    'tamano_fuente_inferior': int(tamano_fuente_inferior)
                }
            except ValueError:
                return HttpResponse("Error: Las coordenadas deben ser números válidos", status=400)
        else:
            return HttpResponse("Error: Se requieren todas las coordenadas del folio", status=400)
        
        # Datos de prueba
        data = {
            'apellido_paterno': 'AGUILA',
            'apellido_materno': 'MENDIETA', 
            'nombres': 'FERNANDO',
            'curp': 'AUMF970410HDFGNR02',
            'puesto': 'TECNICO',
            'nombre_curso': 'CURSO DE PRUEBA',
            'horas_curso': '8',
            'nombre_empresa': 'ADMINITRACION DE CONDOMINIOS MY HOGAR',
            'rfc_empresa': 'ADMINITRACION',
            'representante_legal': 'MARIA DEL CARMEL GARCIA',
            'representante_trabajadores': 'JUAN CARLOS DE ROSA',
            'fecha_inicio': date(2025, 8, 18),
            'fecha_fin': date(2025, 8, 18),
            'instructor_nombre': 'EDUARDO MENDIETA ZUÑIGA',
        }
        
        try:
            # Generar PDF con coordenadas personalizadas del folio
            pdf_content = generar_pdf_con_mapeo_folio(data, 10, coordenadas_folio)
            
            # Crear respuesta HTTP
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="DC3_mapeo_folio.pdf"'
            
            return response
            
        except Exception as e:
            print(f"Error al generar PDF con mapeo de folio: {e}")
            return HttpResponse(f"Error: {e}", status=500)
    
    return HttpResponse("Método no permitido", status=405)

def generar_pdf_con_mapeo_curso(data, plantilla_id, coordenadas_curso):
    """
    Genera un PDF usando la plantilla PDF con coordenadas personalizadas para el nombre del curso
    """
    from PyPDF2 import PdfReader, PdfWriter
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.colors import black
    import io
    from datetime import datetime
    
    # Obtener la plantilla
    plantilla = PlantillaDC3.objects.get(id=plantilla_id, activo=True)
    
    # Leer la plantilla PDF
    with open(plantilla.archivo.path, 'rb') as template_file:
        template_reader = PdfReader(template_file)
        template_page = template_reader.pages[0]
        
        # Crear un nuevo PDF con los datos
        output = PdfWriter()
        
        # Crear un PDF temporal con los datos del formulario
        data_pdf = io.BytesIO()
        c = canvas.Canvas(data_pdf)
        
        # Configurar fuente y tamaño
        c.setFont("Helvetica", 10)
        
        # Coordenadas fijas para otros campos
        posiciones = {
            'nombres': (225, 620),
            'puesto': (77, 578),
            'horas_curso': (54, 416),
            'nombre_empresa': (200, 525),
            'representante_legal': (225, 302),
            'representante_trabajadores': (400, 302),
            'instructor_nombre': (50, 302),
        }
        
        # Escribir campos normales
        for campo, (x, y) in posiciones.items():
            if campo == 'nombres':
                # Combinar nombre completo: APELLIDOS + NOMBRES
                apellido_paterno = data.get('apellido_paterno', '')
                apellido_materno = data.get('apellido_materno', '')
                nombres = data.get('nombres', '')
                nombre_completo = f"{apellido_paterno} {apellido_materno} {nombres}".strip()
                c.drawString(x, y, nombre_completo)
            else:
                valor = data.get(campo, '')
                if hasattr(valor, 'strftime'):  # Verificar si es una fecha
                    valor = valor.strftime('%d/%m/%Y')
                c.drawString(x, y, str(valor))
        
        # Escribir el nombre del curso con coordenadas personalizadas
        valor_curso = data.get('nombre_curso', '')
        x_curso = coordenadas_curso['x']
        y_curso = coordenadas_curso['y']
        ancho_maximo = coordenadas_curso['ancho_maximo']
        alto_linea = coordenadas_curso['alto_linea']
        fuente_base = coordenadas_curso['fuente_base']
        
        print(f"DEBUG - Escribiendo curso: '{valor_curso}' en coordenadas ({x_curso}, {y_curso})")
        print(f"DEBUG - Configuración: ancho={ancho_maximo}, alto_linea={alto_linea}, fuente={fuente_base}")
        
        # Dividir el texto en palabras
        palabras = valor_curso.split()
        lineas = []
        linea_actual = ""
        
        for palabra in palabras:
            # Probar si la palabra cabe en la línea actual
            texto_prueba = linea_actual + " " + palabra if linea_actual else palabra
            c.setFont("Helvetica", fuente_base)
            ancho_texto = c.stringWidth(texto_prueba, "Helvetica", fuente_base)
            
            if ancho_texto <= ancho_maximo:
                linea_actual = texto_prueba
            else:
                if linea_actual:
                    lineas.append(linea_actual)
                linea_actual = palabra
        
        # Agregar la última línea
        if linea_actual:
            lineas.append(linea_actual)
        
        # Si no hay líneas, usar el texto original
        if not lineas:
            lineas = [valor_curso]
        
        print(f"DEBUG - Líneas generadas: {len(lineas)}")
        for i, linea in enumerate(lineas):
            print(f"DEBUG - Línea {i+1}: '{linea}'")
        
        # Escribir cada línea
        for i, linea in enumerate(lineas):
            y_linea = y_curso - (i * alto_linea)
            c.setFont("Helvetica", fuente_base)
            c.drawString(x_curso, y_linea, linea)
            print(f"DEBUG - Escrita línea {i+1} en Y={y_linea}")
        
        # Restablecer la fuente a la predeterminada
        c.setFont("Helvetica", 10)
        
        c.save()
        data_pdf.seek(0)
        
        # Combinar la plantilla con los datos
        data_reader = PdfReader(data_pdf)
        data_page = data_reader.pages[0]
        
        # Superponer los datos sobre la plantilla
        template_page.merge_page(data_page)
        output.add_page(template_page)
        
        # Proteger el PDF con contraseña
        # output = proteger_pdf_con_contraseña(output)  # DESHABILITADO para permitir extracción de texto
        
        # Generar el PDF final
        result_pdf = io.BytesIO()
        output.write(result_pdf)
        result_pdf.seek(0)
        
        return result_pdf.getvalue()

def generar_pdf_con_mapeo_folio(data, plantilla_id, coordenadas_folio):
    """
    Genera un PDF usando la plantilla PDF con coordenadas personalizadas para el folio
    """
    from PyPDF2 import PdfReader, PdfWriter
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.colors import black, Color
    import io
    from datetime import datetime
    
    # Obtener la plantilla
    plantilla = PlantillaDC3.objects.get(id=plantilla_id, activo=True)
    
    # Leer la plantilla PDF
    with open(plantilla.archivo.path, 'rb') as template_file:
        template_reader = PdfReader(template_file)
        template_page = template_reader.pages[0]
        
        # Crear un nuevo PDF con los datos
        output = PdfWriter()
        
        # Crear un PDF temporal con los datos del formulario
        data_pdf = io.BytesIO()
        c = canvas.Canvas(data_pdf)
        
        # Configurar fuente y tamaño
        c.setFont("Helvetica", 10)
        
        # Coordenadas fijas para otros campos
        posiciones = {
            'nombres': (225, 620),
            'puesto': (77, 578),
            'nombre_curso': (114, 450),
            'horas_curso': (54, 416),
            'nombre_empresa': (200, 525),
            'representante_legal': (225, 302),
            'representante_trabajadores': (400, 302),
            'instructor_nombre': (50, 302),
        }
        
        # Escribir campos normales
        for campo, (x, y) in posiciones.items():
            if campo == 'nombres':
                # Combinar nombre completo: APELLIDOS + NOMBRES
                apellido_paterno = data.get('apellido_paterno', '')
                apellido_materno = data.get('apellido_materno', '')
                nombres = data.get('nombres', '')
                nombre_completo = f"{apellido_paterno} {apellido_materno} {nombres}".strip()
                c.drawString(x, y, nombre_completo)
            else:
                valor = data.get(campo, '')
                if hasattr(valor, 'strftime'):  # Verificar si es una fecha
                    valor = valor.strftime('%d/%m/%Y')
                c.drawString(x, y, str(valor))
        
        # Generar folio único
        folio = generar_folio_unico(data)
        
        # Agregar folio con coordenadas personalizadas
        x_superior = coordenadas_folio['x_superior']
        y_superior = coordenadas_folio['y_superior']
        x_inferior = coordenadas_folio['x_inferior']
        y_inferior = coordenadas_folio['y_inferior']
        tamano_fuente_superior = coordenadas_folio['tamano_fuente_superior']
        tamano_fuente_inferior = coordenadas_folio['tamano_fuente_inferior']
        
        # Configurar color negro sólido
        c.setFillColor(Color(0, 0, 0, alpha=1.0))
        
        # Agregar folio en la esquina superior derecha
        c.setFont("Helvetica-Bold", tamano_fuente_superior)
        c.drawString(x_superior, y_superior, f"FOLIO: {folio}")
        
        # Agregar folio en la parte inferior central
        c.setFont("Helvetica-Bold", tamano_fuente_inferior)
        c.drawString(x_inferior, y_inferior, f"FOLIO: {folio}")
        
        # Restaurar color
        c.setFillColor(Color(0, 0, 0, alpha=1))
        
        c.save()
        data_pdf.seek(0)
        
        # Combinar la plantilla con los datos
        data_reader = PdfReader(data_pdf)
        data_page = data_reader.pages[0]
        
        # Superponer los datos sobre la plantilla
        template_page.merge_page(data_page)
        output.add_page(template_page)
        
        # Proteger el PDF con contraseña
        # output = proteger_pdf_con_contraseña(output)  # DESHABILITADO para permitir extracción de texto
        
        # Generar el PDF final
        result_pdf = io.BytesIO()
        output.write(result_pdf)
        result_pdf.seek(0)
        
        return result_pdf.getvalue()