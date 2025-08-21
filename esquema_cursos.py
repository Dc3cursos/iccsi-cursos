#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Esquema de Cursos - Distribución de Horas
=========================================

Este script genera una tabla que muestra cómo distribuir las horas totales
de los cursos en bloques de 8 horas por día, desde 16 hasta 200 horas.
"""

def generar_esquema_cursos():
    """
    Genera el esquema de cursos con distribución de horas en bloques de 8 horas por día.
    
    Returns:
        list: Lista de tuplas con (horas_totales, dias_necesarios)
    """
    esquema = []
    
    # Generar desde 16 hasta 200 horas en intervalos de 8
    for horas in range(16, 201, 8):
        # Calcular días necesarios (siempre redondeando hacia arriba)
        dias = (horas + 7) // 8  # Equivalente a math.ceil(horas / 8)
        esquema.append((horas, dias))
    
    return esquema

def imprimir_tabla(esquema):
    """
    Imprime la tabla del esquema de cursos en formato tabular.
    
    Args:
        esquema (list): Lista de tuplas con (horas_totales, dias_necesarios)
    """
    print("=" * 60)
    print("ESQUEMA DE CURSOS - DISTRIBUCIÓN DE HORAS")
    print("=" * 60)
    print("| {:^25} | {:^25} |".format("Total de Horas del Curso", "Número de Días Necesarios"))
    print("|" + "-" * 27 + "|" + "-" * 27 + "|")
    
    for horas, dias in esquema:
        print("| {:^25} | {:^25} |".format(f"{horas} horas", f"{dias} días"))
    
    print("=" * 60)
    print(f"Total de combinaciones: {len(esquema)}")
    print("=" * 60)

def generar_html_tabla(esquema):
    """
    Genera una tabla HTML del esquema de cursos.
    
    Args:
        esquema (list): Lista de tuplas con (horas_totales, dias_necesarios)
    
    Returns:
        str: Código HTML de la tabla
    """
    html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Esquema de Cursos - Distribución de Horas</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 12px;
            text-align: center;
            border: 1px solid #ddd;
        }
        th {
            background-color: #3498db;
            color: white;
            font-weight: bold;
        }
        tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        tr:hover {
            background-color: #e3f2fd;
        }
        .summary {
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 Esquema de Cursos - Distribución de Horas</h1>
        <table>
            <thead>
                <tr>
                    <th>Total de Horas del Curso</th>
                    <th>Número de Días Necesarios</th>
                </tr>
            </thead>
            <tbody>
"""
    
    for horas, dias in esquema:
        html += f"""
                <tr>
                    <td><strong>{horas} horas</strong></td>
                    <td><strong>{dias} días</strong></td>
                </tr>"""
    
    html += f"""
            </tbody>
        </table>
        <div class="summary">
            <h3>📊 Resumen</h3>
            <p><strong>Total de combinaciones:</strong> {len(esquema)} cursos</p>
            <p><strong>Rango de horas:</strong> 16 - 200 horas</p>
            <p><strong>Intervalo:</strong> 8 horas</p>
            <p><strong>Jornada diaria:</strong> 8 horas</p>
        </div>
    </div>
</body>
</html>"""
    
    return html

def main():
    """Función principal que ejecuta el esquema de cursos."""
    print("🎓 Generando esquema de cursos...")
    
    # Generar el esquema
    esquema = generar_esquema_cursos()
    
    # Imprimir tabla en consola
    imprimir_tabla(esquema)
    
    # Generar archivo HTML
    html_content = generar_html_tabla(esquema)
    
    # Guardar archivo HTML
    with open('esquema_cursos.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n✅ Archivo HTML generado: esquema_cursos.html")
    print("🌐 Abre el archivo en tu navegador para ver la tabla formateada.")

if __name__ == "__main__":
    main()
