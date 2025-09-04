from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Curso, Inscripcion, Pago, CostoCurso
from .forms import PagoForm
import uuid


@login_required
def lista_cursos_con_precio(request):
    """Lista de cursos con precios"""
    cursos = Curso.objects.all()
    
    # Obtener o crear costos para cada curso
    for curso in cursos:
        costo, created = CostoCurso.objects.get_or_create(
            curso=curso,
            defaults={'precio': 380.00, 'moneda': 'MXN'}
        )
        curso.precio = costo.precio
    
    context = {
        'cursos': cursos,
    }
    return render(request, 'cursos/lista_cursos_con_precio.html', context)


@login_required
def detalle_curso_con_precio(request, curso_id):
    """Detalle del curso con precio y opciones de pago"""
    curso = get_object_or_404(Curso, id=curso_id)
    
    # Obtener o crear costo del curso
    costo, created = CostoCurso.objects.get_or_create(
        curso=curso,
        defaults={'precio': 380.00, 'moneda': 'MXN'}
    )
    
    # Verificar si el usuario ya está inscrito
    inscripcion_existente = Inscripcion.objects.filter(
        alumno=request.user,
        curso=curso
    ).first()
    
    # Verificar si ya pagó
    pago_completado = False
    if inscripcion_existente:
        try:
            pago = inscripcion_existente.pago
            pago_completado = pago.es_pagado
        except Pago.DoesNotExist:
            pass
    
    context = {
        'curso': curso,
        'costo': costo,
        'inscripcion_existente': inscripcion_existente,
        'pago_completado': pago_completado,
    }
    return render(request, 'cursos/detalle_curso_con_precio.html', context)


@login_required
def inscribirse_y_pagar(request, curso_id):
    """Inscribirse al curso y mostrar opciones de pago"""
    curso = get_object_or_404(Curso, id=curso_id)
    
    # Verificar si ya está inscrito
    inscripcion_existente = Inscripcion.objects.filter(
        alumno=request.user,
        curso=curso
    ).first()
    
    if inscripcion_existente:
        messages.warning(request, 'Ya estás inscrito en este curso.')
        return redirect('detalle_curso_con_precio', curso_id=curso_id)
    
    # Obtener costo del curso
    costo, created = CostoCurso.objects.get_or_create(
        curso=curso,
        defaults={'precio': 380.00, 'moneda': 'MXN'}
    )
    
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            # Crear inscripción
            inscripcion = Inscripcion.objects.create(
                alumno=request.user,
                curso=curso
            )
            
            # Crear pago
            pago = Pago.objects.create(
                inscripcion=inscripcion,
                monto=costo.precio,
                metodo_pago=form.cleaned_data['metodo_pago'],
                estado='pendiente'
            )
            
            messages.success(request, 'Inscripción creada. Procede con el pago.')
            return redirect('procesar_pago', pago_id=pago.id)
    else:
        form = PagoForm()
    
    context = {
        'curso': curso,
        'costo': costo,
        'form': form,
    }
    return render(request, 'cursos/inscribirse_y_pagar.html', context)


@login_required
def procesar_pago(request, pago_id):
    """Procesar el pago del curso"""
    pago = get_object_or_404(Pago, id=pago_id, inscripcion__alumno=request.user)
    
    if pago.es_pagado:
        messages.info(request, 'Este pago ya fue completado.')
        return redirect('detalle_curso_con_precio', curso_id=pago.inscripcion.curso.id)
    
    if request.method == 'POST':
        # Simular procesamiento de pago
        referencia = f"PAY-{uuid.uuid4().hex[:8].upper()}"
        pago.completar_pago(referencia)
        
        messages.success(request, f'Pago completado exitosamente. Referencia: {referencia}')
        return redirect('detalle_curso_con_precio', curso_id=pago.inscripcion.curso.id)
    
    context = {
        'pago': pago,
        'curso': pago.inscripcion.curso,
    }
    return render(request, 'cursos/procesar_pago.html', context)


@login_required
def mis_cursos_pagados(request):
    """Lista de cursos pagados del usuario"""
    # Usar select_related para optimizar las consultas
    pagos = Pago.objects.filter(
        inscripcion__alumno=request.user,
        estado='completado'
    ).select_related('inscripcion__curso')
    
    cursos_pagados = []
    for pago in pagos:
        cursos_pagados.append({
            'inscripcion': pago.inscripcion,
            'pago': pago,
            'curso': pago.inscripcion.curso
        })
    
    context = {
        'cursos_pagados': cursos_pagados,
    }
    return render(request, 'cursos/mis_cursos_pagados.html', context)


@login_required
def historial_pagos(request):
    """Historial de pagos del usuario"""
    pagos = Pago.objects.filter(inscripcion__alumno=request.user).order_by('-creado')
    
    context = {
        'pagos': pagos,
    }
    return render(request, 'cursos/historial_pagos.html', context)


@login_required
def acceder_curso_pagado(request, curso_id):
    """Acceder al contenido del curso después del pago"""
    curso = get_object_or_404(Curso, id=curso_id)
    
    # Verificar que el usuario esté inscrito y haya pagado
    inscripcion = get_object_or_404(
        Inscripcion,
        alumno=request.user,
        curso=curso
    )
    
    try:
        pago = inscripcion.pago
        if not pago.es_pagado:
            messages.error(request, 'Debes completar el pago para acceder al curso.')
            return redirect('detalle_curso_con_precio', curso_id=curso_id)
    except Pago.DoesNotExist:
        messages.error(request, 'No se encontró el pago para este curso.')
        return redirect('detalle_curso_con_precio', curso_id=curso_id)
    
    # Aquí puedes agregar la lógica para mostrar el contenido del curso
    context = {
        'curso': curso,
        'inscripcion': inscripcion,
        'pago': pago,
    }
    return render(request, 'cursos/acceder_curso_pagado.html', context)


# API endpoints para procesamiento de pagos
@csrf_exempt
@require_POST
def webhook_pago(request):
    """Webhook para recibir confirmaciones de pago"""
    # Aquí implementarías la lógica para recibir confirmaciones
    # de tu proveedor de pagos (PayPal, Stripe, etc.)
    
    # Por ahora, simulamos una confirmación exitosa
    pago_id = request.POST.get('pago_id')
    referencia = request.POST.get('referencia')
    
    try:
        pago = Pago.objects.get(id=pago_id)
        pago.completar_pago(referencia)
        return JsonResponse({'status': 'success'})
    except Pago.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Pago no encontrado'}, status=404)


@login_required
def cancelar_pago(request, pago_id):
    """Cancelar un pago pendiente"""
    pago = get_object_or_404(Pago, id=pago_id, inscripcion__alumno=request.user)
    
    if pago.estado == 'pendiente':
        pago.estado = 'cancelado'
        pago.save()
        messages.success(request, 'Pago cancelado exitosamente.')
    else:
        messages.error(request, 'No se puede cancelar este pago.')
    
    return redirect('historial_pagos')
