import json
import re
from pathlib import Path


CATALOGO_PATH = Path(__file__).resolve().parents[1] / "cursos_por_organizacion.json"
BACKUP_PATH = Path(str(CATALOGO_PATH).replace('.json', '.backup.json'))


def normalize_spaces(text: str) -> str:
    return " ".join((text or "").split())


def should_join(prev_title: str, next_title: str) -> bool:
    if not prev_title or not next_title:
        return False
    p = prev_title.strip()
    n = next_title.strip()

    # Casos claros detectados en el catálogo
    # 1) NOM-... cortado antes del año
    if ("NOM-" in p) and p.endswith("-") and re.match(r"^\d{4}[,\s]", n):
        return True

    # 2) Frases cortadas tipo "... DE LAS" + "INSTALACIONES ..."
    if p.upper().endswith(" DE LAS") and n.upper().startswith("INSTALACIONES"):
        return True

    # 3) Frases cortadas tipo "... EN" + "LOS ..."
    if p.upper().endswith(" EN") and n.upper().startswith("LOS"):
        return True

    # 4) Otorgar continuidad si la primera termina en coma y la segunda empieza con palabra
    #    que normalmente completa la frase
    if p.endswith(",") and re.match(r"^(LOS|LAS|LA|EL|INSTALACIONES|CONDICIONES|CONSTRUCCION|ELECTRICAS)\b", n, re.I):
        return True

    return False


def join_titles(prev_title: str, next_title: str) -> str:
    p = prev_title.rstrip()
    n = next_title.lstrip()
    if p.endswith("-"):
        # Concatenar directamente tras guion (caso NOM-011-STPS- + 2001, ...)
        merged = p + n
    else:
        merged = p + " " + n
    return normalize_spaces(merged)


def limpiar_catalogo(data: dict) -> tuple[dict, int]:
    total_uniones = 0
    nuevo = {}
    for org, cursos in (data or {}).items():
        if not isinstance(cursos, list):
            nuevo[org] = cursos
            continue
        arreglada = []
        i = 0
        while i < len(cursos):
            actual = cursos[i]
            if i + 1 < len(cursos):
                siguiente = cursos[i + 1]
                t1 = str(actual.get("curso", ""))
                t2 = str(siguiente.get("curso", ""))
                if should_join(t1, t2):
                    # Unir títulos
                    horas1 = actual.get("horas")
                    horas2 = siguiente.get("horas")
                    merged_title = join_titles(t1, t2)
                    merged_horas = None
                    if isinstance(horas1, int) and isinstance(horas2, int):
                        merged_horas = max(horas1, horas2)
                    elif isinstance(horas1, int):
                        merged_horas = horas1
                    elif isinstance(horas2, int):
                        merged_horas = horas2
                    else:
                        merged_horas = None
                    arreglada.append({"curso": merged_title, "horas": merged_horas})
                    total_uniones += 1
                    i += 2
                    continue
            # Si no se une, normalizar espacios del título actual
            actual = dict(actual)
            actual["curso"] = normalize_spaces(str(actual.get("curso", "")))
            arreglada.append(actual)
            i += 1
        nuevo[org] = arreglada
    return nuevo, total_uniones


def main() -> None:
    if not CATALOGO_PATH.exists():
        raise SystemExit(f"No se encontró {CATALOGO_PATH}")
    try:
        data = json.loads(CATALOGO_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"Error leyendo JSON: {exc}")

    limpio, uniones = limpiar_catalogo(data)

    # Respaldo
    if not BACKUP_PATH.exists():
        BACKUP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    CATALOGO_PATH.write_text(json.dumps(limpio, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Hecho. Títulos unidos: {uniones}. Archivo actualizado: {CATALOGO_PATH.name}")


if __name__ == "__main__":
    main()



