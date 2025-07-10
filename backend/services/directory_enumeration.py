import requests

COMMON_DIRS = [
    'admin', 'login', 'dashboard', 'api', 'uploads', 'images', 'css', 'js', 'config', 'backup'
]

def detect_directories(host, port=80):
    scheme = 'https' if port == 443 else 'http'
    base_url = f"{scheme}://{host}"

    found_dirs = []

    for d in COMMON_DIRS:
        url = f"{base_url}/{d}"
        try:
            resp = requests.get(url, timeout=3)
            if resp.status_code == 200:
                found_dirs.append(d)
        except requests.RequestException:
            # Ignoramos errores de conexión, timeout, etc.
            pass

    return found_dirs
