#!/usr/bin/env python3
# Script temporal para arreglar la función inscribirse_curso

import re

def fix_inscripcion_function():
    # Leer el archivo
    with open('iccsi/cursos/views.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Definir el texto que queremos reemplazar (desde la línea problemática hasta el final del bloque)
    old_block = '''                apellidos_list = apellidos.split()
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
        
        return redirect('mis_cursos')'''
    
    # Texto comentado de reemplazo
    new_block = '''        #         apellidos_list = apellidos.split()
        #         if len(apellidos_list) >= 2:
        #             apellido_paterno = apellidos_list[0]
        #             apellido_materno = ' '.join(apellidos_list[1:])
        #         else:
        #             apellido_paterno = apellidos_list[0]
        #             apellido_materno = ''
        #     else:
        #         apellido_paterno = ''
        #         apellido_materno = ''
        #     
        #     # Crear datos para el certificado
        #     data = {
        #         'apellido_paterno': apellido_paterno,
        #         'apellido_materno': apellido_materno,
        #         'nombres': nombres,
        #         'curp': user.curp if hasattr(user, 'curp') else '',
        #         'puesto': user.puesto if hasattr(user, 'puesto') else 'EMPLEADO',
        #         'nombre_curso': curso.nombre,  # NOMBRE DEL CURSO DONDE SE INSCRIBIÓ
        #         'horas_curso': str(curso.duracion_horas) if curso.duracion_horas else '0',
        #         'nombre_empresa': user.empresa.nombre if hasattr(user, 'empresa') and user.empresa else 'EMPRESA',
        #         'rfc_empresa': user.empresa.rfc if hasattr(user, 'empresa') and user.empresa else 'RFC',
        #         'representante_legal': user.representante_legal if hasattr(user, 'representante_legal') else 'REPRESENTANTE LEGAL',
        #         'representante_trabajadores': user.representante_trabajadores if hasattr(user, 'representante_trabajadores') else 'REPRESENTANTE TRABAJADORES',
        #         'fecha_inicio': curso.fecha_creacion.date(),
        #         'fecha_fin': curso.fecha_creacion.date(),
        #         'instructor_nombre': curso.profesor.get_full_name() if curso.profesor else 'INSTRUCTOR',
        #     }
        #     
        #     print(f"DEBUG - Nombre del curso: {curso.nombre}")
        #     print(f"DEBUG - Datos del certificado: {data}")
        #     
        #     # Obtener la plantilla según la organización del curso
        #     if curso.organizacion and curso.organizacion.nombre == "Fraternidad Migratoria":
        #         plantilla_id = 10  # Plantilla de Fraternidad Migratoria
        #     elif curso.organizacion and curso.organizacion.nombre == "CPI":
        #         plantilla_id = 11  # Plantilla de CPI
        #     else:
        #         # Fallback a Fraternidad Migratoria si no hay organización o es otra
        #         plantilla_id = 10
        #     
        #     # Coordenadas para caracteres individuales (las que configuraste)
        #     coordenadas_caracteres = {
        #         # CURP (18 caracteres)
        #         'curp_0': (43, 593), 'curp_1': (58, 593), 'curp_2': (72, 593), 'curp_3': (88, 593),
        #         'curp_4': (102, 593), 'curp_5': (117, 593), 'curp_6': (132, 593), 'curp_7': (145, 593),
        #         'curp_8': (158, 593), 'curp_9': (172, 593), 'curp_10': (187, 593), 'curp_11': (201, 593),
        #         'curp_12': (217, 593), 'curp_13': (233, 593), 'curp_14': (250, 593), 'curp_15': (265, 593),
        #         'curp_16': (279, 593), 'curp_17': (297, 593),
        #         
        #         # RFC (13 caracteres)
        #         'rfc_0': (45, 496), 'rfc_1': (58, 496), 'rfc_2': (72, 496), 'rfc_3': (90, 496),
        #         'rfc_4': (118, 496), 'rfc_5': (132, 496), 'rfc_6': (144, 496), 'rfc_7': (157, 496),
        #         'rfc_8': (172, 496), 'rfc_9': (186, 496), 'rfc_10': (217, 496), 'rfc_11': (233, 496),
        #         'rfc_12': (250, 496),
        #         
        #         # Fecha Inicio (solo las posiciones con coordenadas válidas)
        #         'fecha_ini_0': (260, 416), 'fecha_ini_1': (277, 416), 'fecha_ini_2': (292, 416),
        #         'fecha_ini_3': (308, 416), 'fecha_ini_5': (327, 416), 'fecha_ini_6': (347, 416),
        #         'fecha_ini_8': (368, 416), 'fecha_ini_9': (390, 416),
        #         
        #         # Fecha Fin (solo las posiciones con coordenadas válidas)
        #         'fecha_fin_0': (431, 416), 'fecha_fin_1': (450, 416), 'fecha_fin_2': (470, 416),
        #         'fecha_fin_3': (487, 416), 'fecha_fin_5': (510, 416), 'fecha_fin_6': (530, 416),
        #         'fecha_fin_8': (550, 416), 'fecha_fin_9': (570, 416)
        #     }
        #     
        #     # Verificar si ya existe un certificado para esta inscripción
        #     if CertificadoDC3.objects.filter(inscripcion=inscripcion).exists():
        #         print(f"DEBUG - Ya existe un certificado para esta inscripción: {inscripcion.id}")
        #         return redirect('mis_cursos')
        #     
        #     # Crear el certificado
        #     certificado = CertificadoDC3.objects.create(
        #         inscripcion=inscripcion,
        #         empresa=empresa_default,
        #         apellido_paterno=apellido_paterno,
        #         apellido_materno=apellido_materno,
        #         nombres=nombres,
        #         nombre_completo=f"{apellido_paterno} {apellido_materno} {nombres}".strip(),
        #         curp=data['curp'],
        #         puesto=data['puesto'],
        #         horas_curso=curso.duracion_horas if curso.duracion_horas else 4
        #     )
        #     
        #     # Guardar el PDF en el certificado
        #     from django.core.files.base import ContentFile
        #     nombre_archivo = f"DC3_{apellido_paterno}_{apellido_materno}_{nombres}_{curso.nombre}_{timezone.now().strftime('%Y%m%d')}.pdf"
        #     certificado.archivo_pdf.save(nombre_archivo, ContentFile(pdf_content), save=True)
        #     
        #     print(f"Certificado generado automáticamente para {user.username} en curso {curso.nombre}")
        #     print(f"PDF guardado como: {certificado.archivo_pdf.name}")
        #     
        #     print(f"Certificado generado automáticamente para {user.username} en curso {curso.nombre}")
        #     
        # except Exception as e:
        #     print(f"Error al generar certificado automático: {e}")
        # 
        # return redirect('mis_cursos')'''
    
    # Reemplazar el contenido
    new_content = content.replace(old_block, new_block)
    
    # Escribir el archivo corregido
    with open('iccsi/cursos/views.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Archivo corregido exitosamente")

if __name__ == "__main__":
    fix_inscripcion_function()
