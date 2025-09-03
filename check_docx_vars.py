import sys
import json
from pathlib import Path


EXPECTED_VARS = {
    'APELLIDO_PATERNO',
    'APELLIDO_MATERNO',
    'NOMBRES',
    'CURP',
    'OCUPACION',
    'PUESTO',
    'RAZON_SOCIAL',
    'RFC',
    'NOMBRE_CURSO',
    'HORAS',
    'DIA_INICIO',
    'MES_INICIO',
    'ANIO_INICIO',
    'DIA_FIN',
    'MES_FIN',
    'ANIO_FIN',
    'AREA_TEMATICA',
    'AGENTE_CAPACITADOR',
    'REGISTRO_AGENTE',
    'INSTRUCTOR_NOMBRE',
    'ORGANIZACION_NOMBRE',
    'FECHA_EMISION',
    'VIGENCIA',
    'EMPRESA_REPRESENTANTE_LEGAL',
    'EMPRESA_REPRESENTANTE_TRABAJADORES',
    'LOGO',
}


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python tools/check_docx_vars.py <path-to-docx>")
        return 2

    try:
        from docxtpl import DocxTemplate
    except Exception as exc:
        print(json.dumps({
            'ok': False,
            'error': f'docxtpl not installed: {exc}',
        }))
        return 1

    path = Path(sys.argv[1])
    if not path.exists():
        print(json.dumps({'ok': False, 'error': f'File not found: {path.as_posix()}'}))
        return 1

    try:
        doc = DocxTemplate(path.as_posix())
        found = set(doc.get_undeclared_template_variables())
    except Exception as exc:
        print(json.dumps({'ok': False, 'error': f'Failed to parse template: {exc}'}))
        return 1

    missing = sorted(EXPECTED_VARS - found)
    unknown = sorted(found - EXPECTED_VARS)

    print(json.dumps({
        'ok': True,
        'file': path.as_posix(),
        'total_found': len(found),
        'found': sorted(found),
        'missing': missing,
        'unknown': unknown,
        'hint_expected': sorted(EXPECTED_VARS),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())


