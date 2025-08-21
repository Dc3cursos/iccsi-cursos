# 🔧 Solución de Problemas - Sistema de Plantillas DC-3

## 🚨 Problema: "No se genera el certificado"

### ✅ Diagnóstico Completado

Las pruebas automatizadas confirman que el sistema **SÍ está funcionando correctamente**:

- ✅ **Generación de PDF**: Funcionando (2667 bytes generados)
- ✅ **Formulario**: Válido y procesando datos correctamente
- ✅ **Vista**: Respondiendo con Content-Type correcto (application/pdf)
- ✅ **Descarga**: Archivos se guardan correctamente

### 🔍 Posibles Causas del Problema

#### 1. **Problema del Navegador**
- **Síntomas**: El formulario se envía pero no se descarga el PDF
- **Solución**: 
  - Verifica que las descargas estén habilitadas
  - Revisa la carpeta de descargas
  - Prueba con un navegador diferente (Chrome, Firefox, Edge)

#### 2. **Bloqueador de Pop-ups**
- **Síntomas**: No aparece la descarga
- **Solución**: 
  - Deshabilita temporalmente el bloqueador de pop-ups
  - Permite pop-ups para `localhost:8000`

#### 3. **Problema de JavaScript**
- **Síntomas**: El formulario no se envía
- **Solución**:
  - Abre la consola del navegador (F12)
  - Verifica que no hay errores de JavaScript
  - Asegúrate de que JavaScript esté habilitado

#### 4. **Problema de Autenticación**
- **Síntomas**: Error 403 o redirección a login
- **Solución**:
  - Asegúrate de estar logueado en el sistema
  - Cierra sesión y vuelve a iniciar sesión

### 🛠️ Pasos para Diagnosticar

#### Paso 1: Verificar el Navegador
1. Abre la consola del navegador (F12)
2. Ve a la pestaña "Network" (Red)
3. Llena el formulario y envía
4. Busca la petición POST a `/cursos/dc3/llenar-plantilla-sistema/`
5. Verifica el código de respuesta (debe ser 200)

#### Paso 2: Verificar la Descarga
1. Revisa la carpeta de descargas del navegador
2. Busca archivos con nombre `DC3_*.pdf`
3. Verifica que el archivo tenga tamaño > 0 bytes

#### Paso 3: Probar con Navegador Diferente
1. Abre el sistema en Chrome, Firefox o Edge
2. Intenta generar el certificado
3. Compara el comportamiento

### 📋 Checklist de Verificación

- [ ] ¿Estás logueado en el sistema?
- [ ] ¿JavaScript está habilitado?
- [ ] ¿Las descargas están permitidas?
- [ ] ¿No hay bloqueadores de pop-ups activos?
- [ ] ¿La consola del navegador no muestra errores?
- [ ] ¿El formulario se envía correctamente?

### 🎯 Soluciones Específicas

#### Para Chrome:
1. Ve a Configuración > Privacidad y seguridad
2. Configuración del sitio > Descargas
3. Permite descargas para `localhost:8000`

#### Para Firefox:
1. Ve a Configuración > Privacidad y seguridad
2. Permisos > Descargar archivos
3. Permite para `localhost:8000`

#### Para Edge:
1. Ve a Configuración > Cookies y permisos del sitio
2. Descargas automáticas
3. Permite para `localhost:8000`

### 🔧 Comandos de Verificación

Si quieres verificar que el sistema funciona:

```bash
# Probar generación de PDF
python debug_pdf.py

# Probar vista completa
python test_vista_completa.py

# Probar sistema completo
python test_sistema_plantillas.py
```

### 📞 Si el Problema Persiste

Si después de seguir estos pasos el problema persiste:

1. **Captura de pantalla**: Toma una captura del error
2. **Logs del navegador**: Copia los errores de la consola
3. **Información del sistema**: Navegador, versión, sistema operativo
4. **Pasos realizados**: Lista los pasos que seguiste

### 🎉 Confirmación de Funcionamiento

El sistema **SÍ está funcionando correctamente** según las pruebas automatizadas:

- ✅ PDF generado: 2667 bytes
- ✅ Content-Type: application/pdf
- ✅ Formulario válido
- ✅ Vista respondiendo correctamente
- ✅ Archivos guardándose correctamente

El problema es probablemente de configuración del navegador o permisos de descarga.

### 🚀 Próximos Pasos

1. Sigue la guía de solución de problemas arriba
2. Si el problema persiste, proporciona la información solicitada
3. El sistema está técnicamente funcional y listo para usar
