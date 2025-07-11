from routes.celery_worker import celery_app
import json

@celery_app.task(bind=True)

def run_vuln_scan(self, target):
    from app import create_app
    from models import db, VulnScan
    import subprocess, re
    from datetime import datetime
    from utils.reports import save_report_json, save_report_html

    try:
        result = subprocess.check_output(
            ["nmap", "-sV", "--script", "vulners", target],
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        parsed_vulns = []
        current_service = None
        for line in result.splitlines():
            port_service = re.match(r"^(\d+/tcp)\s+\w+\s+(\S+)\s+(.*)$", line)
            if port_service:
                current_service = {
                    "port": port_service.group(1),
                    "service": port_service.group(2),
                    "version": port_service.group(3),
                    "cves": []
                }
                parsed_vulns.append(current_service)
            elif "CVE-" in line and current_service:
                cve_match = re.findall(r"(CVE-\d{4}-\d+)\s+(\d+\.\d+)\s+(https?://\S+)", line)
                for cve_id, score, url in cve_match:
                    current_service["cves"].append({
                        "id": cve_id,
                        "score": score,
                        "url": url
                    })

        json_report_path = save_report_json(target, parsed_vulns)
        html_report_path = save_report_html(target, parsed_vulns)

        app = create_app()
        with app.app_context():
            vuln_scan = VulnScan(
                host=target,
                scan_type="vulnerability",
                timestamp=datetime.now(),
                vulnerabilities=json.dumps(parsed_vulns),  # <-- Aquí la clave
                json_report_path=json_report_path,
                html_report_path=html_report_path
            )
            try:
                db.session.add(vuln_scan)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return {
                    "error": "Error al guardar en base de datos",
                    "details": str(e)
                }

            return {
                "host": target,
                "vulnerabilities": parsed_vulns,
                "json_report_path": json_report_path,
                "html_report_path": html_report_path,
                "db_id": vuln_scan.id
            }

    except subprocess.CalledProcessError as e:
        return {
            "error": "Error ejecutando nmap",
            "details": e.output
        }
