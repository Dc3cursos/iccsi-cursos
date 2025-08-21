# 🔍 GUÍA SIMPLE: CÓMO VERIFICAR CERTIFICADOS DC-3

## 📋 Resumen

Esta guía te explica de manera **SIMPLE y EFECTIVA** cómo saber si un certificado DC-3 es **AUTÉNTICO** (emitido por ICCSI) o **FALSO**.

---

## ✅ CERTIFICADO AUTÉNTICO (VÁLIDO)

### **Características Visuales en el PDF:**
- 🔒 **Candado de seguridad** en la barra de herramientas del lector PDF
- 📄 **Estado**: "Protegido" o "Solo Lectura"
- ⚠️ **No permite edición** de campos
- 📝 **Texto de verificación** visible en la parte inferior: "CERTIFICADO OFICIAL ICCSI"
- 🔢 **Código de verificación único** presente (ejemplo: "CODIGO: A1B2C3D4E5F6")
- 🏷️ **Código ICCSI** en las esquinas (ejemplo: "ICCSI-A1B2C3D4E5F6")

### **En el Sistema Web de Verificación:**
- ✅ **Resultado**: "CERTIFICADO AUTÉNTICO"
- 🛡️ **Nivel**: 3-6/6
- 💧 **Marcas de Agua**: Múltiples detectadas
- 🔐 **Seguridad**: MÁXIMO

---

## ❌ CERTIFICADO FALSO (INVÁLIDO)

### **Características Visuales en el PDF:**
- 🔓 **Sin candado de seguridad**
- 📝 **Permite edición libre** de campos
- 🚫 **Sin texto de verificación** en la parte inferior
- 🔢 **Sin código de verificación único**
- 🏷️ **Sin código ICCSI** en las esquinas

### **En el Sistema Web de Verificación:**
- ❌ **Resultado**: "CERTIFICADO NO AUTÉNTICO"
- 🛡️ **Nivel**: 0-2/6
- 💧 **Marcas de Agua**: No encontradas
- 🔓 **Seguridad**: BAJO

---

## 🔍 CÓMO VERIFICAR (PASOS SIMPLES)

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
- 🛡️ Nivel de autenticidad: 3-6/6
- 💧 Se muestran las marcas de agua detectadas
- 🔐 Nivel de seguridad: MÁXIMO

#### **Si es FALSO:**
- ❌ Aparece mensaje rojo: "CERTIFICADO NO AUTÉNTICO"
- 🛡️ Nivel de autenticidad: 0-2/6
- ⚠️ Mensaje: "No se encontraron marcas de agua ICCSI"
- 🔓 Nivel de seguridad: BAJO

---

## 🎯 ELEMENTOS QUE VERIFICA EL SISTEMA

| Elemento | Puntos | Descripción |
|----------|--------|-------------|
| **"CERTIFICADO OFICIAL ICCSI"** | 2 | Texto principal de verificación |
| **"CODIGO: [código]"** | 2 | Código único de verificación |
| **"ICCSI-[código]"** | 1 | Código en esquinas del PDF |
| **"VERIFICABLE EN:"** | 1 | Texto de verificación web |
| **Encriptación** | 1 | Protección del PDF |

**Total máximo: 6 puntos**
**Mínimo para ser auténtico: 3 puntos**

---

## 🔧 VERIFICACIÓN MANUAL (SIN SISTEMA WEB)

### **Revisar en el PDF:**
1. **Abrir el PDF** en cualquier lector
2. **Buscar en la parte inferior**:
   - ✅ "CERTIFICADO OFICIAL ICCSI"
   - ✅ "VERIFICABLE EN: www.iccsi.edu.mx"
   - ✅ "CODIGO: [12 caracteres]"
3. **Buscar en las esquinas**:
   - ✅ "ICCSI-[12 caracteres]"
4. **Verificar protección**:
   - ✅ Candado de seguridad visible
   - ✅ No permite edición

### **Si encuentras estos elementos = AUTÉNTICO**
### **Si NO encuentras estos elementos = FALSO**

---

## 📞 SOPORTE RÁPIDO

### **Si tienes dudas:**
1. **Verificar en el sistema web** primero
2. **Revisar características visuales** del PDF
3. **Contactar a ICCSI** si el resultado es inesperado

### **Información de Contacto:**
- **Institución**: ICCSI - Instituto de Capacitación y Certificación
- **Sistema**: Plataforma de Verificación de Certificados DC-3
- **URL**: `http://127.0.0.1:8000/cursos/verificar-certificado/`

---

## 🎯 CONCLUSIÓN SIMPLE

**Un certificado es AUTÉNTICO si:**
- ✅ El sistema web lo marca como "AUTÉNTICO"
- ✅ Tiene nivel de autenticidad 3-6/6
- ✅ Muestra candado de seguridad en el PDF
- ✅ No permite edición
- ✅ Tiene texto de verificación visible
- ✅ Tiene código de verificación único

**Un certificado es FALSO si:**
- ❌ El sistema web lo marca como "NO AUTÉNTICO"
- ❌ Tiene nivel de autenticidad 0-2/6
- ❌ No tiene candado de seguridad
- ❌ Permite edición libre
- ❌ No tiene texto de verificación
- ❌ No tiene código de verificación

---

## 🚀 SISTEMA IMPLEMENTADO

- **Protección Múltiple**: Marcas de agua, encriptación, restricciones
- **Verificación Automática**: Sistema web que detecta autenticidad
- **Interfaz Clara**: Resultados visuales fáciles de entender
- **Códigos Únicos**: Cada certificado tiene un código de verificación único
- **Protección Contra Edición**: PDFs protegidos contra modificaciones

**¡Ahora puedes distinguir fácilmente entre certificados auténticos y falsos!**

---

*Guía generada automáticamente - Sistema de Verificación ICCSI v2025*
