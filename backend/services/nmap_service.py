# backend/services/nmap_service.py

import nmap
import logging

def scan_service(host, port, protocol='tcp'):
    """
    Escanea un servicio concreto en un host para detectar versión y banner.
    """
    nm = nmap.PortScanner()
    try:
        logging.info(f"Escaneando servicio {host}:{port}/{protocol}")

        args = f"-sV -p {port} -T4"
        nm.scan(hosts=host, arguments=args)

        if host not in nm.all_hosts():
            return {"error": f"Host {host} no responde"}

        service_info = {}
        if protocol in nm[host].all_protocols():
            proto_data = nm[host][protocol]
            if port in proto_data:
                port_data = proto_data[port]
                service_info = {
                    "port": port,
                    "state": port_data['state'],
                    "service": port_data.get('name', ''),
                    "version": port_data.get('version', ''),
                    "product": port_data.get('product', ''),
                    "extra_info": port_data.get('extrainfo', ''),
                    "cpe": port_data.get('cpe', '')
                }
            else:
                return {"error": f"Puerto {port}/{protocol} no encontrado"}
        else:
            return {"error": f"Protocolo {protocol} no encontrado"}

        return {"host": host, "service_info": service_info}

    except Exception as e:
        logging.error(f"Error al escanear servicio {host}:{port}: {e}")
        return {"error": f"Error al escanear servicio: {str(e)}"}
