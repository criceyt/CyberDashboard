from flask import Blueprint, request, jsonify
from services.os_detect import detect_os
import logging

os_scan_bp = Blueprint('os_scan', __name__)

@os_scan_bp.route('/os-scan', methods=['POST'])
def os_scan():
    data = request.get_json()
    if not data or 'host' not in data:
        return jsonify({"error": "Falta el parámetro 'host' en JSON"}), 400

    host = data['host']
    logging.info(f"Petición de detección SO para host={host}")

    result = detect_os(host)
    return jsonify(result)
