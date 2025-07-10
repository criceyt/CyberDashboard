
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .vuln_scan import VulnScan  # importa aquí tu modelo
