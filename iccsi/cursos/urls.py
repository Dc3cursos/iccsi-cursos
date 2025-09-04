from django.urls import path
from . import views
from .pago_views import (
    lista_cursos_con_precio, detalle_curso_con_precio, inscribirse_y_pagar,
    procesar_pago, mis_cursos_pagados, historial_pagos, acceder_curso_pagado,
    webhook_pago, cancelar_pago
)
from .stripe_views import (
    crear_pago_stripe, confirmar_pago_stripe, exito_pago_stripe,
    cancelar_pago_stripe, webhook_stripe, dashboard_pagos_profesor
)



urlpatterns = [
    path('', views.lista_cursos, name='lista_cursos'),
    path('curso/<int:curso_id>/', views.detalle_curso, name='detalle_curso'),
    path('curso/<int:curso_id>/inscribirse/', views.inscribirse_curso, name='inscribirse_curso'),
    path('mis-cursos/', views.mis_cursos, name='mis_cursos'),
    path('crear/', views.crear_curso, name='crear_curso'),
    path('editar/<int:curso_id>/', views.editar_curso, name='editar_curso'),
    path('eliminar/<int:curso_id>/', views.eliminar_curso, name='eliminar_curso'),
    
    # URLs para certificados DC-3
    path('dc3/llenar-plantilla-sistema/', views.llenar_plantilla_dc3_sistema, name='llenar_plantilla_dc3_sistema'),
    path('dc3/previsualizar/', views.previsualizar_certificado, name='previsualizar_certificado'),
    path('dc3/plantilla-preview/<int:plantilla_id>/', views.obtener_plantilla_preview, name='obtener_plantilla_preview'),
    
    # URLs para plantillas PDF
    path('dc3/plantilla-pdf/<str:tipo_plantilla>/', views.descargar_plantilla_pdf, name='descargar_plantilla_pdf'),
    path('dc3/procesar-pdf/', views.procesar_pdf_llenado, name='procesar_pdf_llenado'),
    path('dc3/llenar-en-sistema/', views.llenar_pdf_en_sistema, name='llenar_pdf_en_sistema'),
    path('dc3/llenar-en-sistema/<int:certificado_id>/', views.llenar_pdf_en_sistema, name='llenar_pdf_en_sistema_con_id'),
    
    # URLs para mapeo de coordenadas
    path('dc3/mapear-coordenadas/', views.mapear_coordenadas, name='mapear_coordenadas'),
    path('dc3/generar-con-coordenadas/', views.generar_con_coordenadas, name='generar_con_coordenadas'),
    
    # URLs para mapeo de caracteres individuales
    path('dc3/mapeo-caracteres-individuales/', views.mapeo_caracteres_individuales, name='mapeo_caracteres_individuales'),
    path('dc3/generar-con-caracteres-individuales/', views.generar_con_caracteres_individuales, name='generar_con_caracteres_individuales'),
    
    # URL para descargar certificados generados automáticamente
    path('certificado/<int:inscripcion_id>/descargar/', views.descargar_certificado_inscripcion, name='descargar_certificado_inscripcion'),
    
    # URL para descargar certificados
    path('certificado/<int:inscripcion_id>/', views.descargar_certificado, name='descargar_certificado'),
    
    # URLs para mapeo específico del nombre del curso
    path('dc3/mapeo-curso/', views.mapeo_curso, name='mapeo_curso'),
    path('dc3/generar-con-mapeo-curso/', views.generar_con_mapeo_curso, name='generar_con_mapeo_curso'),
    
    # URLs para mapeo específico del folio
    path('dc3/mapeo-folio/', views.mapeo_folio, name='mapeo_folio'),
    path('dc3/generar-con-mapeo-folio/', views.generar_con_mapeo_folio, name='generar_con_mapeo_folio'),
    
    # URL para verificar autenticidad de certificados
    path('verificar-certificado/', views.verificar_certificado, name='verificar_certificado'),

    # URLs del sistema de pagos
    path('cursos-con-precio/', lista_cursos_con_precio, name='lista_cursos_con_precio'),
    path('curso-con-precio/<int:curso_id>/', detalle_curso_con_precio, name='detalle_curso_con_precio'),
    path('inscribirse-y-pagar/<int:curso_id>/', inscribirse_y_pagar, name='inscribirse_y_pagar'),
    path('procesar-pago/<int:pago_id>/', procesar_pago, name='procesar_pago'),
    path('mis-cursos-pagados/', mis_cursos_pagados, name='mis_cursos_pagados'),
    path('historial-pagos/', historial_pagos, name='historial_pagos'),
    path('acceder-curso/<int:curso_id>/', acceder_curso_pagado, name='acceder_curso_pagado'),
    path('webhook-pago/', webhook_pago, name='webhook_pago'),
    path('cancelar-pago/<int:pago_id>/', cancelar_pago, name='cancelar_pago'),
    
    # URLs de Stripe
    path('stripe/crear-pago/<int:curso_id>/', crear_pago_stripe, name='crear_pago_stripe'),
    path('stripe/confirmar-pago/<int:pago_id>/', confirmar_pago_stripe, name='confirmar_pago_stripe'),
    path('stripe/exito-pago/<int:pago_id>/', exito_pago_stripe, name='exito_pago_stripe'),
    path('stripe/cancelar-pago/<int:pago_id>/', cancelar_pago_stripe, name='cancelar_pago_stripe'),
    path('stripe/webhook/', webhook_stripe, name='webhook_stripe'),
    path('dashboard-pagos/', dashboard_pagos_profesor, name='dashboard_pagos_profesor'),
]