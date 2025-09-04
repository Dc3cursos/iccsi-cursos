import stripe
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from django.utils import timezone
from .models import Curso, Inscripcion, Pago, CostoCurso
from .forms import PagoForm

# Configurar Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def crear_pago_stripe(request, curso_id):
    """Crear un Payment Intent de Stripe para un curso"""
    curso = get_object_or_404(Curso, id=curso_id)
    costo, _ = CostoCurso.objects.get_or_create(
        curso=curso, 
        defaults={'precio': 380.00, 'moneda': 'MXN'}
    )
    
    # Crear o obtener inscripción
    inscripcion, created = Inscripcion.objects.get_or_create(
        usuario=request.user,
        curso=curso,
        defaults={'fecha_inscripcion': timezone.now()}
    )
    
    # Verificar si ya existe un pago completado
    if Pago.objects.filter(inscripcion=inscripcion, estado='completado').exists():
        messages.info(request, "Ya has pagado este curso. Puedes acceder a él.")
        return redirect('acceder_curso_pagado', curso_id=curso.id)
    
    try:
        # Crear Payment Intent en Stripe
        payment_intent = stripe.PaymentIntent.create(
            amount=int(costo.precio * 100),  # Stripe usa centavos
            currency='mxn',
            metadata={
                'curso_id': curso.id,
                'usuario_id': request.user.id,
                'inscripcion_id': inscripcion.id
            },
            description=f"Pago por curso: {curso.nombre}",
            receipt_email=request.user.email if request.user.email else None,
        )
        
        # Crear o actualizar el pago en nuestra base de datos
        pago, created = Pago.objects.get_or_create(
            inscripcion=inscripcion,
            defaults={
                'monto': costo.precio,
                'metodo_pago': 'tarjeta',
                'estado': 'pendiente',
                'stripe_payment_intent_id': payment_intent.id,
                'stripe_client_secret': payment_intent.client_secret,
                'stripe_status': payment_intent.status
            }
        )
        
        if not created:
            # Actualizar pago existente
            pago.stripe_payment_intent_id = payment_intent.id
            pago.stripe_client_secret = payment_intent.client_secret
            pago.stripe_status = payment_intent.status
            pago.save()
        
        return JsonResponse({
            'client_secret': payment_intent.client_secret,
            'payment_intent_id': payment_intent.id,
            'pago_id': pago.id
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def confirmar_pago_stripe(request, pago_id):
    """Confirmar un pago de Stripe"""
    pago = get_object_or_404(Pago, id=pago_id, inscripcion__usuario=request.user)
    
    if pago.estado == 'completado':
        messages.info(request, "Este pago ya ha sido completado.")
        return redirect('acceder_curso_pagado', curso_id=pago.inscripcion.curso.id)
    
    context = {
        'pago': pago,
        'curso': pago.inscripcion.curso,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    
    return render(request, 'cursos/confirmar_pago_stripe.html', context)

@login_required
def exito_pago_stripe(request, pago_id):
    """Página de éxito después del pago"""
    pago = get_object_or_404(Pago, id=pago_id, inscripcion__usuario=request.user)
    
    if pago.estado != 'completado':
        # Verificar el estado en Stripe
        try:
            payment_intent = stripe.PaymentIntent.retrieve(pago.stripe_payment_intent_id)
            if payment_intent.status == 'succeeded':
                pago.estado = 'completado'
                pago.fecha_pago = timezone.now()
                pago.stripe_status = payment_intent.status
                pago.save()
                messages.success(request, "¡Pago completado exitosamente!")
            else:
                messages.warning(request, f"El pago está en estado: {payment_intent.status}")
        except Exception as e:
            messages.error(request, f"Error al verificar el pago: {str(e)}")
    
    context = {
        'pago': pago,
        'curso': pago.inscripcion.curso,
    }
    
    return render(request, 'cursos/exito_pago_stripe.html', context)

@login_required
def cancelar_pago_stripe(request, pago_id):
    """Cancelar un pago de Stripe"""
    pago = get_object_or_404(Pago, id=pago_id, inscripcion__usuario=request.user)
    
    if pago.estado == 'pendiente':
        try:
            # Cancelar Payment Intent en Stripe
            if pago.stripe_payment_intent_id:
                stripe.PaymentIntent.cancel(pago.stripe_payment_intent_id)
            
            pago.estado = 'cancelado'
            pago.save()
            messages.info(request, "El pago ha sido cancelado.")
        except Exception as e:
            messages.error(request, f"Error al cancelar el pago: {str(e)}")
    else:
        messages.warning(request, "Solo se pueden cancelar pagos pendientes.")
    
    return redirect('historial_pagos')

@csrf_exempt
def webhook_stripe(request):
    """Webhook para recibir notificaciones de Stripe"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    
    # Manejar eventos de Stripe
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        actualizar_pago_completado(payment_intent['id'])
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        actualizar_pago_fallido(payment_intent['id'])
    
    return HttpResponse(status=200)

def actualizar_pago_completado(payment_intent_id):
    """Actualizar pago como completado"""
    try:
        pago = Pago.objects.get(stripe_payment_intent_id=payment_intent_id)
        pago.estado = 'completado'
        pago.fecha_pago = timezone.now()
        pago.stripe_status = 'succeeded'
        pago.save()
    except Pago.DoesNotExist:
        pass

def actualizar_pago_fallido(payment_intent_id):
    """Actualizar pago como fallido"""
    try:
        pago = Pago.objects.get(stripe_payment_intent_id=payment_intent_id)
        pago.estado = 'cancelado'
        pago.stripe_status = 'failed'
        pago.save()
    except Pago.DoesNotExist:
        pass

@login_required
def dashboard_pagos_profesor(request):
    """Dashboard para que el profesor vea los pagos de sus cursos"""
    if request.user.rol != 'profesor':
        messages.error(request, "No tienes permisos para acceder a esta página.")
        return redirect('home')
    
    # Obtener pagos de los cursos del profesor
    pagos = Pago.objects.filter(
        inscripcion__curso__profesor=request.user,
        estado='completado'
    ).select_related('inscripcion__curso', 'inscripcion__usuario').order_by('-fecha_pago')
    
    # Calcular estadísticas
    total_ingresos = sum(pago.monto for pago in pagos)
    total_cursos_vendidos = pagos.count()
    
    # Estadísticas por mes
    from django.db.models import Sum
    from django.utils import timezone
    from datetime import timedelta
    
    # Últimos 6 meses
    meses = []
    for i in range(6):
        fecha = timezone.now() - timedelta(days=30*i)
        mes_pagos = pagos.filter(fecha_pago__month=fecha.month, fecha_pago__year=fecha.year)
        meses.append({
            'mes': fecha.strftime('%B %Y'),
            'ingresos': sum(p.monto for p in mes_pagos),
            'cursos': mes_pagos.count()
        })
    
    context = {
        'pagos': pagos,
        'total_ingresos': total_ingresos,
        'total_cursos_vendidos': total_cursos_vendidos,
        'meses': meses,
    }
    
    return render(request, 'cursos/dashboard_pagos_profesor.html', context)
