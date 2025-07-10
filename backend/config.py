import os
class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://flaskuser:flaskpassword@localhost/cyberdashboard"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave_por_defecto_para_desarrollo')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super_secret_jwt_key')

    # Configuración Celery
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

    # Opcional: ajustes extra para Celery
    CELERY_TASK_SERIALIZER = "json"
    CELERY_ACCEPT_CONTENT = ["json"]
    CELERY_RESULT_SERIALIZER = "json"
    CELERY_TIMEZONE = "Europe/Madrid"
    CELERY_ENABLE_UTC = True
