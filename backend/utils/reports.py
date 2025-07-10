import json
import os
import datetime as dt  # 👈 Evita sobrescritura del módulo estándar

def save_report_json(target, report_data):
    # Crear carpeta si no existe
    os.makedirs("reports/vuln/json", exist_ok=True)
    # Generar timestamp con datetime estándar
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"vuln_report_{target}_{timestamp}.json"
    filepath = os.path.join("reports/vuln/json", filename)

    # Guardar el JSON
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4)

    return filepath

def save_report_html(target, report_data):
    # Si report_data es una lista, la metemos dentro de un dict con clave 'vulnerabilities'
    if isinstance(report_data, list):
        report_data = {"vulnerabilities": report_data}

    # Crear carpeta si no existe
    os.makedirs("reports/vuln/HTML", exist_ok=True)
    # Generar timestamp con datetime estándar
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"vuln_report_{target}_{timestamp}.html"
    filepath = os.path.join("reports/vuln/HTML", filename)

    # Estilos atractivos para el HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Informe de Vulnerabilidades - {target}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background: #f7f9fc;
                color: #333;
            }}
            header {{
                background: #2c3e50;
                color: #fff;
                padding: 20px;
                text-align: center;
            }}
            h1 {{
                margin: 0;
                font-size: 24px;
            }}
            .container {{
                padding: 20px;
            }}
            .summary {{
                background: #ecf0f1;
                padding: 10px;
                margin-bottom: 20px;
                border-radius: 8px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                padding: 12px;
                border: 1px solid #ddd;
                text-align: left;
            }}
            th {{
                background-color: #34495e;
                color: white;
            }}
            .cve-critical {{
                background: #e74c3c;
                color: #fff;
            }}
            .cve-high {{
                background: #e67e22;
                color: #fff;
            }}
            .cve-medium {{
                background: #f1c40f;
            }}
            .cve-low {{
                background: #2ecc71;
                color: #fff;
            }}
            .cve-link {{
                text-decoration: none;
                color: #2980b9;
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>Informe de Vulnerabilidades</h1>
            <p>Host escaneado: {target}</p>
            <p>Fecha: {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </header>
        <div class="container">
            <div class="summary">
                <h2>Resumen del escaneo</h2>
                <p>Servicios detectados: {len(report_data.get('vulnerabilities', []))}</p>
            </div>
            <h2>Detalle de vulnerabilidades</h2>
            <table>
                <tr>
                    <th>Puerto</th>
                    <th>Servicio</th>
                    <th>Versión</th>
                    <th>CVE</th>
                    <th>Score</th>
                </tr>"""

    # Añadir filas a la tabla
    for vuln in report_data.get("vulnerabilities", []):
        for cve in vuln.get("cves", []):
            # Clasificar severidad por score
            score = float(cve.get("score", 0))
            if score >= 9.0:
                severity_class = "cve-critical"
            elif score >= 7.0:
                severity_class = "cve-high"
            elif score >= 4.0:
                severity_class = "cve-medium"
            else:
                severity_class = "cve-low"

            html_content += f"""
                <tr>
                    <td>{vuln['port']}</td>
                    <td>{vuln['service']}</td>
                    <td>{vuln['version']}</td>
                    <td class="{severity_class}">
                        <a href="{cve['url']}" class="cve-link">{cve['id']}</a>
                    </td>
                    <td>{cve['score']}</td>
                </tr>"""

    html_content += """
            </table>
        </div>
    </body>
    </html>
    """

    # Guardar el archivo HTML
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)

    return filepath

