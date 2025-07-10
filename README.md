# 🛡️ CyberDashboard - Backend 🔥

Un potente **backend para un dashboard de ciberseguridad**, diseñado para ejecutar y gestionar herramientas de análisis de red desde una API RESTful.
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)  
[![Flask](https://img.shields.io/badge/Flask-2.3-lightgrey.svg)](https://flask.palletsprojects.com/)  
[![Celery](https://img.shields.io/badge/Celery-5.x-green.svg)](https://docs.celeryq.dev/)  
[![MIT License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## ✨ Características

- ✅ API REST para escaneos de red y servicios  
- ✅ Integración con Celery para tareas asíncronas y procesado paralelo  
- ✅ Endpoints disponibles:  
  - 📂 Escaneo de subdirectorios (`/api/dir-scan`)  
  - 🖥️ Detección del sistema operativo remoto (`/api/os-scan`)  
  - ⚡ Escaneo rápido de servicios (`/api/scan`)  
  - 🔥 Búsqueda de vulnerabilidades (`/api/vuln-scan`)  
- ✅ Preparado para expandirse con más funciones de hacking ético 🕵️‍♂️  

---

## 🚀 Instalación y ejecución (todo en uno)

```powershell
# Clonar el repositorio y navegar al backend
git clone https://github.com/TU-USUARIO/CyberDashboard.git
cd CyberDashboard/backend

# Crear y activar entorno virtual
python -m venv venv
.\venv\Scripts\activate      # Windows


# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el servidor Flask
python app.py

Abrir otra terminal y ejecutar Celery:

$env:PYTHONPATH=(Get-Location); celery -A routes.celery_worker.celery_app worker --loglevel=info --pool=solo

🧪 Ejemplos de peticiones API con PowerShell

# Escaneo de subdirectorios
$targetHost = "http://ekain.duckdns.org"
$body = @{ host = $targetHost } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/dir-scan" -Method POST -Body $body -ContentType "application/json"

# Detección del sistema operativo remoto
$body = @{ host = "192.168.1.145" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/os-scan" -Method POST -Body $body -ContentType "application/json"

# Escaneo rápido de servicios en un rango
$bodyObject = @{ target = "192.168.1.128/25"; mode = "fast" }
$body = $bodyObject | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/scan" -Method POST -Body $body -ContentType "application/json"

# Búsqueda de vulnerabilidades
$body = @{ host = "192.168.1.145" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/vuln-scan" -Method POST -Body $body -ContentType "application/json"
