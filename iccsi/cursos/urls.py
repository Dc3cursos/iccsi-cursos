from django.urls import path
from . import views

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
]