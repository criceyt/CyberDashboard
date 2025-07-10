import nmap
import logging

def detect_os(host):
    nm = nmap.PortScanner()
    try:
        logging.info(f"Iniciando detección de SO para host: {host}")
        # Escaneo con detección OS, requiere permisos elevados (sudo)
        nm.scan(hosts=host, arguments='-O')
        
        hosts = nm.all_hosts()
        if not hosts:
            logging.info(f"No se detectó host vivo para {host}")
            return {"error": "Host no encontrado o no está vivo"}

        host = hosts[0]  # Sólo uno, ya que es una IP única

        if 'osmatch' in nm[host]:
            os_matches = nm[host]['osmatch']
            if os_matches:
                # Devolvemos el nombre del OS más probable
                os_name = os_matches[0]['name']
                accuracy = os_matches[0]['accuracy']
                logging.info(f"SO detectado para {host}: {os_name} (Precisión: {accuracy}%)")
                return {"host": host, "os": os_name, "accuracy": accuracy}
            else:
                logging.info(f"No se pudo detectar SO para {host}")
                return {"host": host, "os": "Desconocido"}
        else:
            logging.info(f"No hay información OS para {host}")
            return {"host": host, "os": "Desconocido"}

    except Exception as e:
        logging.error(f"Error en detección de SO: {e}")
        return {"error": str(e)}
