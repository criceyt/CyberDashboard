import re

def is_valid_ip(ip):
    """
    Comprueba si la cadena es una IP IPv4 válida.
    """
    pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    if re.match(pattern, ip):
        # Comprobamos que cada octeto esté en el rango 0-255
        return all(0 <= int(part) <= 255 for part in ip.split('.'))
    return False

def is_valid_hostname(hostname):
    """
    Comprueba si la cadena es un nombre de dominio válido.
    """
    if len(hostname) > 253:
        return False
    pattern = r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)$"
    return all(re.match(pattern, part) for part in hostname.split("."))
