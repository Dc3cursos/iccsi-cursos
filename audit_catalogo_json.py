import json
from pathlib import Path


CATALOGO_PATH = Path(__file__).resolve().parents[1] / "cursos_por_organizacion.json"


SUSPICIOUS_ENDINGS = [
    " DE",
    " DE LAS",
    " DE LA",
    " EN",
    " Y",
    " PARA",
    " CON",
    " SOBRE",
    " DEL",
    " A",
]


def is_suspicious(title: str) -> bool:
    if not title:
        return False
    up = title.strip().upper()
    return any(up.endswith(suf) for suf in SUSPICIOUS_ENDINGS)


def main() -> None:
    data = json.loads(CATALOGO_PATH.read_text(encoding="utf-8"))
    total_items = 0
    total_with_int_hours = 0

    title_to_orgs: dict[str, set[str]] = {}
    suspicious_samples: list[str] = []
    suspicious_count = 0

    for org, cursos in data.items():
        if not isinstance(cursos, list):
            continue
        for item in cursos:
            total_items += 1
            nombre = str(item.get("curso", ""))
            horas = item.get("horas")
            if isinstance(horas, int):
                total_with_int_hours += 1
            if is_suspicious(nombre):
                suspicious_count += 1
                if len(suspicious_samples) < 20:
                    suspicious_samples.append(f"[{org}] {nombre}")
            title_to_orgs.setdefault(nombre, set()).add(org)

    duplicated_titles = [t for t, orgs in title_to_orgs.items() if len(orgs) > 1]

    print("Resumen del catálogo JSON:")
    print(f"- Total de entradas: {total_items}")
    print(f"- Con horas (int): {total_with_int_hours}")
    print(f"- Títulos potencialmente cortados (sospechosos): {suspicious_count}")
    if suspicious_samples:
        print("  Ejemplos:")
        for s in suspicious_samples:
            print("   ", s)
    print(f"- Títulos repetidos entre múltiples organizaciones: {len(duplicated_titles)}")
    if duplicated_titles:
        print("  Ejemplos:")
        for t in duplicated_titles[:20]:
            orgs = ", ".join(sorted(title_to_orgs[t]))
            print(f"    {t}  ->  {orgs}")


if __name__ == "__main__":
    main()


