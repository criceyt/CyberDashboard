import os
from datetime import timedelta

class Config:
    # Base de datos
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://flaskuser:flaskpassword@localhost/cyberdashboard"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask y claves secretas
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave_por_defecto_para_desarrollo')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super_secret_jwt_key')

    # JWT Config
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)  # Tokens de acceso duran 15 minutos
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)     # Tokens de refresh duran 1 día
    JWT_TOKEN_LOCATION = ['headers']                  # Dónde busca los tokens (cabeceras)
    JWT_COOKIE_SECURE = False                         # True en producción con HTTPS
    JWT_COOKIE_CSRF_PROTECT = False                   # Activa protección CSRF si usas cookies
    JWT_ALGORITHM = 'HS256'                           # Algoritmo de firma (default HS256)

    # Celery
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
    CELERY_TASK_SERIALIZER = "json"
    CELERY_ACCEPT_CONTENT = ["json"]
    CELERY_RESULT_SERIALIZER = "json"
    CELERY_TIMEZONE = "Europe/Madrid"
    CELERY_ENABLE_UTC = True
