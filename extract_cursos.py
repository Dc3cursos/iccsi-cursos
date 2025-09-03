import fitz  # PyMuPDF
import re
import json

def extraer_cursos_por_organizacion(pdf_path: str) -> dict:
    doc = fitz.open(pdf_path)
    texto_completo = ""
    for pagina in doc:
        texto_completo += pagina.get_text()
    doc.close()

    # Diagnóstico: imprime las primeras 100 líneas del texto extraído
    for i, linea in enumerate(texto_completo.splitlines()):
        if i < 100:
            print(f"LINEA {i+1}: {repr(linea)}")
        else:
            break

    # Separar por organización
    partes = re.split(r"COLOCACI[ÓO]N DE PROYECTOS INDUSTRIALES S\\.?C\\.? DE R\\.?L\\.? DE C\\.?V\\.?", texto_completo, flags=re.IGNORECASE)
    fraternidad_texto = partes[0]
    colocacion_texto = partes[1] if len(partes) > 1 else ""

    def extraer_cursos_tabla(texto, nombre_org):
        cursos = []
        lineas = [l.strip() for l in texto.splitlines() if l.strip()]
        buffer = []
        skip_lines = [nombre_org.upper(), nombre_org.title(), nombre_org.capitalize()]
        registro_pat = re.compile(r"Registro:|REGISTRO:", re.IGNORECASE)
        for linea in lineas:
            if any(linea.startswith(skip) for skip in skip_lines):
                continue
            if registro_pat.search(linea):
                continue
            if linea.lower() in ["curso", "horas"]:
                continue
            # Si la línea es solo un número (horas)
            if re.fullmatch(r"\d{1,3}", linea):
                if buffer:
                    nombre = " ".join(buffer).replace("  ", " ").strip()
                    if len(nombre) > 10:
                        cursos.append({"curso": nombre, "horas": int(linea)})
                    buffer = []
            else:
                buffer.append(linea)
        return cursos

    resultado = {
        "Fraternidad Migratoria": extraer_cursos_tabla(fraternidad_texto, "FRATERNIDAD MIGRATORIA A.C"),
        "Colocación de Proyectos Industriales": extraer_cursos_tabla(colocacion_texto, "COLOCACION DE PROYECTOS INDUSTRIALES S.C. DE R.L. DE C.V")
    }

    with open("cursos_por_organizacion.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    print("¡Extracción completada! Revisa el archivo cursos_por_organizacion.json")
    return resultado

# Ejemplo de uso:
if __name__ == "__main__":
    ruta_pdf = "CATALOGO DE CURSOS.pdf"
    extraer_cursos_por_organizacion(ruta_pdf)