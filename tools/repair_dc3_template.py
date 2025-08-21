import re
import sys
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from zipfile import ZipFile
import io


INVALID_TAG_RE = re.compile(r"\{\{\s*([\s\S]*?)\s*\}\}")
ALLOWED_KEY_RE = re.compile(r"^[A-Z0-9_]+(?:_\d+)?$")


def normalize_variables(text: str) -> str:
    # Arrays de caracteres a variables numeradas RFC_1.., CURP_1..
    text = re.sub(r"\{\{\s*rfc_chars\[(\d+)\]\s*\}\}",
                  lambda m: f"{{{{ RFC_{int(m.group(1)) + 1} }}}}", text)
    text = re.sub(r"\{\{\s*curp_chars\[(\d+)\]\s*\}\}",
                  lambda m: f"{{{{ CURP_{int(m.group(1)) + 1} }}}}", text)

    # Día/Mes/Año por dígito -> DIA_INICIO_1.., MES_FIN_2.., ANIO_INICIO_1..
    def replace_dmy_digits(match: re.Match) -> str:
        unit, when, idx = match.group(1), match.group(2), int(match.group(3))
        unit_up = {"dia": "DIA", "mes": "MES", "anio": "ANIO"}[unit]
        when_up = {"inicio": "INICIO", "fin": "FIN"}[when]
        return f"{{{{ {unit_up}_{when_up}_{idx} }}}}"

    text = re.sub(r"\{\{\s*(dia|mes|anio)_(inicio|fin)_d\[(\d+)\]\s*\}\}",
                  replace_dmy_digits, text)

    # Normalizaciones simples a claves esperadas
    simple_map = {
        "{{ trabajador_nombre }}": "{{ APELLIDO_PATERNO }} {{ APELLIDO_MATERNO }} {{ NOMBRES }}",
        "{{trabajador_nombre}}": "{{ APELLIDO_PATERNO }} {{ APELLIDO_MATERNO }} {{ NOMBRES }}",
        "{{ empresa_razon_social }}": "{{ RAZON_SOCIAL }}",
        "{{empresa_razon_social}}": "{{ RAZON_SOCIAL }}",
        "{{ curso_nombre }}": "{{ NOMBRE_CURSO }}",
        "{{curso_nombre}}": "{{ NOMBRE_CURSO }}",
        "{{ curso_horas }}": "{{ HORAS }}",
        "{{curso_horas}}": "{{ HORAS }}",
        "{{ ocupacion }}": "{{ OCUPACION }}",
        "{{ocupacion}}": "{{ OCUPACION }}",
        "{{ dia_inicio }}": "{{ DIA_INICIO }}",
        "{{dia_inicio}}": "{{ DIA_INICIO }}",
        "{{ mes_inicio }}": "{{ MES_INICIO }}",
        "{{mes_inicio}}": "{{ MES_INICIO }}",
        "{{ anio_inicio }}": "{{ ANIO_INICIO }}",
        "{{anio_inicio}}": "{{ ANIO_INICIO }}",
        "{{ dia_fin }}": "{{ DIA_FIN }}",
        "{{dia_fin}}": "{{ DIA_FIN }}",
        "{{ mes_fin }}": "{{ MES_FIN }}",
        "{{mes_fin}}": "{{ MES_FIN }}",
        "{{ anio_fin }}": "{{ ANIO_FIN }}",
        "{{anio_fin}}": "{{ ANIO_FIN }}",
        "{{ puesto }}": "{{ PUESTO }}",
        "{{puesto}}": "{{ PUESTO }}",
    }
    for src, dst in simple_map.items():
        text = text.replace(src, dst)

    # Quitar '{{ }}' alrededor de etiquetas descriptivas (deben ser texto plano)
    label_patterns = [
        r"\{\{\s*Nombre\s*\(Anotar[\s\S]*?\}\}",
        r"\{\{\s*Nombre\s+del\s+curso\s*\}\}",
        r"\{\{\s*Nombre\s+o\s+razón\s+social[\s\S]*?\}\}",
        r"\{\{\s*Registro\s+Federal\s+de\s+Contribuyentes[\s\S]*?\}\}",
        r"\{\{\s*Clave\s+Única\s+de\s+Registro\s+de\s+Población\s*\}\}",
        # Caso frecuente: "Nombre (Apellido paterno, Apellido materno, Nombre(s))" entre llaves
        r"\{\{\s*Nombre\s*\(Apellido\s+paterno,\s*Apellido\s+materno,\s*Nombre\(s\)\)\s*:?[\s\S]*?\}\}",
        # Patrón genérico de texto largo en español entre llaves (probable etiqueta, no variable)
        r"\{\{\s*[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ,()\-\./:]{10,}\s*\}\}",
    ]
    for pat in label_patterns:
        def strip_braces(m: re.Match) -> str:
            inner = m.group(0)
            # quita {{ y }} si existen
            inner = re.sub(r"^\{\{\s*", "", inner)
            inner = re.sub(r"\s*\}\}$", "", inner)
            return inner

        text = re.sub(pat, strip_braces, text)

    # Eliminar braces de cualquier marcador inválido que no cumpla el patrón permitido
    def sanitize_tag(m: re.Match) -> str:
        inner = (m.group(1) or "").strip()
        # si es permitido, lo dejamos como {{ KEY }} con KEY normalizado
        if ALLOWED_KEY_RE.match(inner):
            return f"{{{{ {inner} }}}}"
        # de lo contrario, devolvemos solo el texto interno sin llaves
        return inner

    text = INVALID_TAG_RE.sub(sanitize_tag, text)

    # Normalizaciones finales de seguridad: colapsar braces duplicados y eliminar restos sueltos
    text = text.replace("{{{{", "{{").replace("}}}}", "}}")
    # Si quedó una llave de cierre/ apertura suelta alrededor de espacios, quítala
    text = re.sub(r"\{\}\s*", "", text)

    return text


def _repair_element(element) -> None:
    """Repara todas las etiquetas dentro del elemento oxml dado (body, header, footer, etc.)."""
    for p in element.iter(qn('w:p')):
        t_nodes = list(p.iter(qn('w:t')))
        if not t_nodes:
            continue
        full_text = ''.join((t.text or '') for t in t_nodes)
        if not full_text:
            continue
        normalized = normalize_variables(full_text)
        t_nodes[0].text = normalized
        for t in t_nodes[1:]:
            t.text = ''


def repair_docx(input_path: Path, output_path: Path) -> None:
    doc = Document(input_path.as_posix())

    # Documento principal
    document_root = doc.element.body.getparent()
    _repair_element(document_root)

    # Encabezados y pies de página de todas las secciones
    try:
        for section in doc.sections:
            if hasattr(section, 'header') and section.header and hasattr(section.header, '_element'):
                _repair_element(section.header._element)
            if hasattr(section, 'footer') and section.footer and hasattr(section.footer, '_element'):
                _repair_element(section.footer._element)
    except Exception:
        # Si python-docx no expone secciones correctamente, continuamos al menos con el cuerpo
        pass

    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output_path.as_posix())

    # Pasada adicional a nivel ZIP/XML para capturar textos en cuadros de texto u otros contenedores no expuestos por python-docx
    try:
        buf_in = Path(output_path).read_bytes()
        with ZipFile(io.BytesIO(buf_in), 'r') as zin:
            out_mem = io.BytesIO()
            with ZipFile(out_mem, 'w') as zout:
                for name in zin.namelist():
                    data = zin.read(name)
                    if name.startswith('word/') and name.endswith('.xml'):
                        try:
                            xml_text = data.decode('utf-8')
                        except UnicodeDecodeError:
                            try:
                                xml_text = data.decode('cp1252')
                            except Exception:
                                xml_text = data.decode('latin-1', errors='ignore')

                        # Aplicar normalizaciones en bruto sobre el XML completo
                        xml_text = normalize_variables(xml_text)
                        data = xml_text.encode('utf-8')
                    zout.writestr(name, data)
            final_bytes = out_mem.getvalue()
        with open(output_path, 'wb') as f:
            f.write(final_bytes)
    except Exception:
        # Si algo falla, dejamos al menos la versión reparada por python-docx
        pass


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python tools/repair_dc3_template.py <input.docx> <output.docx>")
        sys.exit(2)
    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])
    repair_docx(input_file, output_file)
    print(f"Reparado: {input_file} -> {output_file}")


