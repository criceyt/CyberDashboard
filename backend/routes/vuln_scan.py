from flask import Blueprint, request, jsonify
import subprocess
import re
import json
import os
from utils.reports import save_report_json, save_report_html
from datetime import datetime
from .tasks import run_vuln_scan
vuln_scan_bp = Blueprint("vuln_scan", __name__)

@vuln_scan_bp.route("/api/vuln-scan", methods=["POST"])
def vuln_scan():
    data = request.json
    target = data.get("host")

    if not target:
        return jsonify({"error": "No host provided"}), 400

    # Lanzar la tarea asíncrona
    task = run_vuln_scan.delay(target)
    return jsonify({"task_id": task.id}), 202


