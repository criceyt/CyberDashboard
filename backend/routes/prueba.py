from routes.tasks import run_vuln_scan


if __name__ == "__main__":
    target_ip = "127.0.0.1"  # Cambia aquí a la IP o dominio que quieras escanear

    # Enviamos la tarea a Celery
    async_result = run_vuln_scan.delay(target_ip)
    print(f"Tarea enviada con ID: {async_result.id}")

    # Esperamos el resultado (timeout 60s para nmap)
    print("Esperando resultado...")
    try:
        resultado = async_result.get(timeout=60)
        print("Resultado recibido:")
        print(resultado)
    except Exception as e:
        print(f"Error o timeout esperando resultado: {e}")
