# 💳 CONFIGURACIÓN DE PASARELAS DE PAGO EN MÉXICO

## 🎯 Opciones de Pasarelas de Pago para México

### 1. **Stripe** (Recomendado)
- **Comisión**: 3.5% + $2.50 MXN por transacción
- **Tiempo de liquidación**: 2-3 días hábiles
- **Ventajas**: Fácil integración, documentación excelente, soporte en español
- **Desventajas**: Comisión relativamente alta

### 2. **MercadoPago**
- **Comisión**: 3.5% + $2.50 MXN por transacción
- **Tiempo de liquidación**: 1-2 días hábiles
- **Ventajas**: Muy popular en México, múltiples métodos de pago
- **Desventajas**: Interfaz menos intuitiva

### 3. **PayPal**
- **Comisión**: 3.9% + $4.00 MXN por transacción
- **Tiempo de liquidación**: 1-3 días hábiles
- **Ventajas**: Reconocido mundialmente, fácil de usar
- **Desventajas**: Comisión más alta

### 4. **Conekta**
- **Comisión**: 3.5% + $2.50 MXN por transacción
- **Tiempo de liquidación**: 1-2 días hábiles
- **Ventajas**: Mexicano, buen soporte local
- **Desventajas**: Menos documentación

## 🔧 Configuración con Stripe (Recomendado)

### Paso 1: Crear Cuenta en Stripe
1. Ve a [stripe.com](https://stripe.com)
2. Crea una cuenta gratuita
3. Completa la verificación de identidad
4. Configura tu cuenta bancaria para recibir pagos

### Paso 2: Obtener Credenciales
En el dashboard de Stripe:
- **Publishable Key**: `pk_test_...` (para desarrollo)
- **Secret Key**: `sk_test_...` (para desarrollo)
- **Webhook Secret**: Para recibir notificaciones de pagos

### Paso 3: Instalar Dependencias
```bash
pip install stripe django-stripe-payments
```

### Paso 4: Configurar Django Settings
```python
# settings.py
STRIPE_PUBLISHABLE_KEY = 'pk_test_tu_clave_publica'
STRIPE_SECRET_KEY = 'sk_test_tu_clave_secreta'
STRIPE_WEBHOOK_SECRET = 'whsec_tu_webhook_secret'

# Configuración de pagos
STRIPE_CURRENCY = 'mxn'
STRIPE_PAYMENT_METHOD_TYPES = ['card']
```

### Paso 5: Actualizar Modelo de Pago
```python
# models.py
class Pago(models.Model):
    # ... campos existentes ...
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_charge_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_status = models.CharField(max_length=50, blank=True, null=True)
```

### Paso 6: Crear Vistas de Pago
```python
# views.py
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def crear_pago_stripe(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    costo = curso.costo.precio
    
    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=int(costo * 100),  # Stripe usa centavos
            currency='mxn',
            metadata={'curso_id': curso.id, 'usuario_id': request.user.id}
        )
        
        return JsonResponse({
            'client_secret': payment_intent.client_secret,
            'payment_intent_id': payment_intent.id
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
```

## 🔧 Configuración con MercadoPago

### Paso 1: Crear Cuenta
1. Ve a [mercadopago.com.mx](https://mercadopago.com.mx)
2. Crea una cuenta de desarrollador
3. Configura tu cuenta bancaria

### Paso 2: Obtener Credenciales
- **Access Token**: Para procesar pagos
- **Public Key**: Para el frontend
- **Webhook URL**: Para recibir notificaciones

### Paso 3: Instalar SDK
```bash
pip install mercadopago
```

### Paso 4: Configurar Vistas
```python
import mercadopago

def crear_pago_mercadopago(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    costo = curso.costo.precio
    
    sdk = mercadopago.SDK("TU_ACCESS_TOKEN")
    
    preference_data = {
        "items": [
            {
                "title": curso.nombre,
                "quantity": 1,
                "unit_price": float(costo)
            }
        ],
        "back_urls": {
            "success": "http://127.0.0.1:8000/pagos/exito/",
            "failure": "http://127.0.0.1:8000/pagos/fallo/",
            "pending": "http://127.0.0.1:8000/pagos/pendiente/"
        },
        "auto_return": "approved"
    }
    
    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    
    return JsonResponse({
        'preference_id': preference['id'],
        'init_point': preference['init_point']
    })
```

## 🔧 Configuración con PayPal

### Paso 1: Crear Cuenta
1. Ve a [paypal.com/mx](https://paypal.com/mx)
2. Crea una cuenta de negocio
3. Configura tu cuenta bancaria

### Paso 2: Obtener Credenciales
- **Client ID**: Para el frontend
- **Secret**: Para el backend
- **Webhook ID**: Para notificaciones

### Paso 3: Instalar SDK
```bash
pip install paypalrestsdk
```

### Paso 4: Configurar Vistas
```python
import paypalrestsdk

paypalrestsdk.configure({
    "mode": "sandbox",  # Cambiar a "live" para producción
    "client_id": "TU_CLIENT_ID",
    "client_secret": "TU_CLIENT_SECRET"
})

def crear_pago_paypal(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    costo = curso.costo.precio
    
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://127.0.0.1:8000/pagos/exito/",
            "cancel_url": "http://127.0.0.1:8000/pagos/cancelar/"
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": curso.nombre,
                    "sku": f"curso_{curso.id}",
                    "price": str(costo),
                    "currency": "MXN",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": str(costo),
                "currency": "MXN"
            },
            "description": f"Pago por curso: {curso.nombre}"
        }]
    })
    
    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                return JsonResponse({
                    'approval_url': link.href,
                    'payment_id': payment.id
                })
    else:
        return JsonResponse({'error': payment.error}, status=400)
```

## 💰 ¿Dónde Llega el Dinero?

### Stripe:
- **Cuenta bancaria**: Se transfiere a tu cuenta bancaria configurada
- **Frecuencia**: Cada 2-3 días hábiles
- **Mínimo**: No hay mínimo para transferencias
- **Comisión**: Se descuenta automáticamente

### MercadoPago:
- **Cuenta MercadoPago**: Primero llega a tu cuenta de MercadoPago
- **Transferencia bancaria**: Puedes transferir a tu banco cuando quieras
- **Frecuencia**: Transferencias manuales
- **Mínimo**: $100 MXN para transferencias

### PayPal:
- **Cuenta PayPal**: Primero llega a tu cuenta de PayPal
- **Transferencia bancaria**: Transferencias manuales
- **Frecuencia**: Cuando solicites la transferencia
- **Mínimo**: $150 MXN para transferencias

## 🛡️ Seguridad y Webhooks

### Configurar Webhooks
```python
# views.py
@csrf_exempt
def webhook_stripe(request):
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
    
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        # Actualizar estado del pago en tu base de datos
        actualizar_pago_completado(payment_intent['id'])
    
    return HttpResponse(status=200)
```

## 📊 Dashboard de Pagos

### Crear Dashboard para Ver Pagos
```python
@login_required
def dashboard_pagos(request):
    if request.user.rol != 'profesor':
        return redirect('home')
    
    # Obtener pagos de los cursos del profesor
    pagos = Pago.objects.filter(
        inscripcion__curso__profesor=request.user,
        estado='completado'
    ).select_related('inscripcion__curso', 'inscripcion__usuario')
    
    # Calcular estadísticas
    total_ingresos = sum(pago.monto for pago in pagos)
    total_cursos_vendidos = pagos.count()
    
    context = {
        'pagos': pagos,
        'total_ingresos': total_ingresos,
        'total_cursos_vendidos': total_cursos_vendidos,
    }
    
    return render(request, 'cursos/dashboard_pagos.html', context)
```

## 🎯 Recomendación Final

### Para tu caso (cursos de $380 MXN):

1. **Stripe** es la mejor opción porque:
   - Fácil integración con Django
   - Excelente documentación
   - Soporte en español
   - Comisión razonable para montos pequeños
   - Transferencias automáticas

2. **Pasos para implementar**:
   - Crear cuenta en Stripe
   - Configurar credenciales en Django
   - Actualizar el modelo de Pago
   - Implementar las vistas de pago
   - Configurar webhooks
   - Probar en modo sandbox

3. **Configuración de producción**:
   - Cambiar a credenciales de producción
   - Configurar HTTPS
   - Configurar webhooks de producción
   - Configurar dominio real

¿Te gustaría que implemente la integración con Stripe en tu sistema? Es la opción más profesional y fácil de usar.
