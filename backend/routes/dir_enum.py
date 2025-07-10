from flask import Blueprint, request, jsonify
import requests
import logging
import os
import json  # <-- Para guardar el reporte en formato JSON
from datetime import datetime

dir_enum_bp = Blueprint('dir_enum', __name__)

def load_wordlist(filename="wordlists/common.txt"):
    """
    Carga la lista de subdirectorios desde un archivo.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        logging.error(f"Wordlist no encontrada: {filename}")
        return []

def scan_directories(host, wordlist=None):
    """
    Intenta encontrar subdirectorios existentes en un host.
    """
    if wordlist is None:
        wordlist = load_wordlist()
    
    found = []
    for directory in wordlist:
        url = f"{host.rstrip('/')}/{directory}"
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                found.append({"directory": directory, "status": response.status_code})
        except requests.RequestException as e:
            logging.warning(f"No se pudo acceder a {url}: {e}")
    return found

@dir_enum_bp.route('/dir-scan', methods=['POST'])
def dir_scan():
    data = request.get_json()
    if not data or 'host' not in data:
        return jsonify({"error": "Falta el parámetro 'host' en JSON"}), 400

    host = data['host']
    custom_wordlist = data.get('wordlist')  # Permite enviar una lista en la petición

    logging.info(f"Petición de escaneo de directorios para host={host}")

    result = scan_directories(host, wordlist=custom_wordlist)

    # === NUEVO: Guardar reporte ===
    report_dir = os.path.join("reports", "enum", "json")
    os.makedirs(report_dir, exist_ok=True)  # Crea la carpeta si no existe

    safe_host = host.replace("http://", "").replace("https://", "").replace("/", "_")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    report_filename = f"scan-{safe_host}-{timestamp}.json"
    report_path = os.path.join(report_dir, report_filename)

    with open(report_path, "w", encoding="utf-8") as report_file:
        json.dump({"host": host, "found": result}, report_file, indent=2, ensure_ascii=False)

    return jsonify({"found": result, "report": report_path})
