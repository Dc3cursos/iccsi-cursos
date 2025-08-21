# 🔍 GUÍA: CÓMO DISTINGUIR CERTIFICADOS AUTÉNTICOS vs FALSOS

## 📋 Resumen

Esta guía te explica exactamente cómo saber si un certificado DC-3 es **AUTÉNTICO** (emitido por ICCSI) o **FALSO** (modificado o falsificado).

---

## ✅ CERTIFICADO AUTÉNTICO (VÁLIDO)

### **Características Visuales:**
- 🔒 **Candado de seguridad** en la barra de herramientas del lector PDF
- 📄 **Estado**: "Protegido" o "Solo Lectura"
- ⚠️ **No permite edición** de campos o texto
- 📝 **Texto de verificación** visible en la parte inferior: "CERTIFICADO OFICIAL ICCSI"
- 🔢 **Código de verificación único** presente

### **En el Sistema de Verificación Web:**
- ✅ **Resultado**: "CERTIFICADO AUTÉNTICO"
- 🛡️ **Nivel de Autenticidad**: 3-5/5
- 💧 **Marcas de Agua**: Múltiples marcas ICCSI detectadas
- 🔐 **Protección**: Encriptación y restricciones activas

### **Ejemplo de Resultado:**
```
✅ CERTIFICADO AUTÉNTICO
Nivel de Autenticidad: 4/5
Marcas de Agua Detectadas:
  ✅ Marca de agua de verificación ICCSI encontrada
  ✅ Hash de integridad ICCSI encontrado
  ✅ Certificado oficial ICCSI encontrado
  ✅ Texto de verificación oficial encontrado
Nivel de Seguridad: MÁXIMO
```

---

## ❌ CERTIFICADO FALSO/MODIFICADO (INVÁLIDO)

### **Características Visuales:**
- 🔓 **Sin candado de seguridad**
- 📝 **Permite edición libre** de campos
- 🚫 **Sin texto de verificación** en la parte inferior
- 🔢 **Sin código de verificación único**
- ✏️ **Puede ser modificado fácilmente**

### **En el Sistema de Verificación Web:**
- ❌ **Resultado**: "CERTIFICADO NO AUTÉNTICO"
- 🛡️ **Nivel de Autenticidad**: 0-1/5
- 💧 **Marcas de Agua**: No se encontraron marcas ICCSI
- 🔓 **Sin protección**: Sin encriptación o restricciones

### **Ejemplo de Resultado:**
```
❌ CERTIFICADO NO AUTÉNTICO
Nivel de Autenticidad: 0/5
No se encontraron marcas de agua ICCSI
Esto indica que el documento no es auténtico o ha sido modificado
Nivel de Seguridad: BAJO
```

---

## 🔍 CÓMO VERIFICAR

### **Paso 1: Acceder al Sistema**
1. Ir a: `http://127.0.0.1:8000/cursos/verificar-certificado/`
2. Hacer clic en "Verificar Certificado" en el menú principal

### **Paso 2: Subir el PDF**
1. Hacer clic en "Seleccionar Certificado DC-3"
2. Elegir el archivo PDF a verificar
3. Hacer clic en "Verificar Autenticidad"

### **Paso 3: Interpretar Resultados**

#### **Si es AUTÉNTICO:**
- ✅ Aparece mensaje verde: "CERTIFICADO AUTÉNTICO"
- 🛡️ Nivel de autenticidad: 3-5/5
- 💧 Se muestran las marcas de agua detectadas
- 🔐 Nivel de seguridad: MÁXIMO o ALTO

#### **Si es FALSO:**
- ❌ Aparece mensaje rojo: "CERTIFICADO NO AUTÉNTICO"
- 🛡️ Nivel de autenticidad: 0-1/5
- ⚠️ Mensaje: "No se encontraron marcas de agua ICCSI"
- 🔓 Nivel de seguridad: BAJO

---

## 🎯 NIVELES DE SEGURIDAD

| Nivel | Puntuación | Estado | Descripción |
|-------|------------|--------|-------------|
| **MÁXIMO** | 4-5/5 | ✅ Auténtico | Certificado completamente válido |
| **MEDIO** | 2-3/5 | ⚠️ Dudoso | Algunas marcas detectadas |
| **BAJO** | 0-1/5 | ❌ Falso | Probablemente modificado |

---

## 🔧 VERIFICACIÓN TÉCNICA

### **Marcas de Agua que Detecta el Sistema:**
- `ICCSI_VERIFY_[hash]` - Verificación de autenticidad
- `ICCSI_HASH_[hash]` - Hash de integridad
- `ICCSI_DATA_[curp]` - Datos específicos del certificado
- `ICCSI_OFFICIAL_[hash]` - Certificado oficial
- `CERTIFICADO OFICIAL ICCSI` - Texto de verificación
- `CODIGO: [código]` - Código de verificación único

### **Protecciones Detectadas:**
- 🔐 Encriptación 128-bit
- 📝 Restricciones de solo lectura
- 🚫 Protección contra edición
- 💧 Marcas de agua invisibles
- 🔢 Hash de integridad único

---

## 📞 SOPORTE

### **Si tienes dudas:**
1. **Verificar en el sistema web** primero
2. **Revisar características visuales** del PDF
3. **Contactar a ICCSI** si el resultado es inesperado

### **Información de Contacto:**
- **Institución**: ICCSI - Instituto de Capacitación y Certificación
- **Sistema**: Plataforma de Verificación de Certificados DC-3
- **URL**: `http://127.0.0.1:8000/cursos/verificar-certificado/`

---

## 🎯 CONCLUSIÓN

**Un certificado es AUTÉNTICO si:**
- ✅ El sistema web lo marca como "AUTÉNTICO"
- ✅ Tiene nivel de autenticidad 3-5/5
- ✅ Muestra candado de seguridad en el PDF
- ✅ No permite edición
- ✅ Tiene texto de verificación visible

**Un certificado es FALSO si:**
- ❌ El sistema web lo marca como "NO AUTÉNTICO"
- ❌ Tiene nivel de autenticidad 0-1/5
- ❌ No tiene candado de seguridad
- ❌ Permite edición libre
- ❌ No tiene texto de verificación

---

*Guía generada automáticamente - Sistema de Verificación ICCSI v2025*
