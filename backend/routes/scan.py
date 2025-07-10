import os
import json
import ipaddress
import logging
import nmap
from flask import Blueprint, request, jsonify
from services.nmap_service import scan_service
from services.os_detect import detect_os

scan_bp = Blueprint('scan', __name__)

def ensure_report_dir():
    path = "reports/scan/json"
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def save_report(target, data):
    path = ensure_report_dir()
    # Nombre del archivo basado en target y timestamp para evitar colisiones
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"scan_{target.replace('/', '_').replace(':', '_')}_{timestamp}.json"
    filepath = os.path.join(path, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    logging.info(f"Reporte guardado en {filepath}")

def parse_ips(target):
    try:
        # Trata de interpretar como red
        network = ipaddress.ip_network(target, strict=False)
        ips = [str(ip) for ip in network.hosts()]
        return ",".join(ips)
    except ValueError:
        pass

    if '-' in target:
        start_ip, end_ip = target.split('-', 1)
        try:
            start = ipaddress.IPv4Address(start_ip.strip())
            end = ipaddress.IPv4Address(end_ip.strip())
            if end < start:
                raise ValueError("IP final menor que la inicial")

            start_parts = start_ip.strip().split('.')
            end_parts = end_ip.strip().split('.')

            if start_parts[:-1] == end_parts[:-1]:
                base_ip = ".".join(start_parts[:-1])
                start_num = int(start_parts[-1])
                end_num = int(end_parts[-1])

                ips = [f"{base_ip}.{i}" for i in range(start_num, end_num + 1)]
                return ",".join(ips)
            else:
                ips = [str(ipaddress.IPv4Address(ip)) for ip in range(int(start), int(end) + 1)]
                return ",".join(ips)
        except ValueError:
            pass

    return target

def real_scan(targets, mode='fast'):
    nm = nmap.PortScanner()
    try:
        logging.info(f"Iniciando escaneo para target(s): {targets}")

        args = '-T4 -p 1-1024' if mode == 'fast' else '-T4'

        nm.scan(hosts=targets, arguments=args)

        logging.info(f"Escaneo completado para {targets}")

        results = {}

        hosts = nm.all_hosts()
        logging.info(f"Hosts detectados por nmap: {hosts}")

        for host in hosts:
            logging.info(f"Host: {host} - Estado: {nm[host].state()}")
            ports = []
            for proto in nm[host].all_protocols():
                for port in nm[host][proto].keys():
                    state = nm[host][proto][port]['state']
                    service = nm[host][proto][port]['name']
                    if state == 'open':
                        ports.append({str(port): service})
            results[host] = ports

        logging.info(f"Resultados: {results}")

        return results

    except Exception as e:
        logging.error(f"Error al escanear: {e}")
        return None

def scan_target(target, mode="fast"):
    logging.info(f"Iniciando escaneo para target: {target}")
    try:
        result = real_scan(target, mode)
        response = {"success": [{target: result}], "errors": []}
        # Guardar reporte
        save_report(target, response)
        return response
    except Exception as e:
        logging.error(f"Error al escanear '{target}': {str(e)}")
        return {"success": [], "errors": [{target: str(e)}]}

@scan_bp.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    if not data or 'target' not in data:
        return jsonify({"error": "Falta el parámetro 'target' en JSON"}), 400

    target = data['target']
    mode = data.get('mode', 'fast')

    logging.info(f"Petición de escaneo recibida para target={target} modo={mode}")
    result = scan_target(target, mode)
    return jsonify(result)

@scan_bp.route('/service-scan', methods=['POST'])
def service_scan():
    data = request.get_json()
    if not data or 'host' not in data or 'port' not in data:
        return jsonify({"error": "Faltan parámetros obligatorios: host y port"}), 400

    host = data['host']
    port = data['port']
    protocol = data.get('protocol', 'tcp')

    result = scan_service(host, port, protocol)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result), 200
