import os
from flask import Flask
from flasgger import Swagger
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from routes.scan import scan_bp
from routes.os_scan import os_scan_bp
from routes.auth import auth_bp
from routes.dir_enum import dir_enum_bp
from routes.vuln_scan import vuln_scan_bp
from utils.error_handlers import register_error_handlers, register_jwt_error_handlers
from utils.logger import setup_logger
from models import db  # 👈 ya no repitas VulnScan aquí
from routes.celery_worker import init_celery

def create_app():
    app = Flask(__name__)

    # Configuración desde un archivo
    app.config.from_object('config.Config')

    # Extensiones
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)

    # Blueprints
    app.register_blueprint(scan_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(os_scan_bp, url_prefix='/api')
    app.register_blueprint(dir_enum_bp, url_prefix='/api')
    app.register_blueprint(vuln_scan_bp)

    # Utilidades
    register_error_handlers(app)
    register_jwt_error_handlers(app, jwt)
    setup_logger()
    Swagger(app)
    init_celery(app)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
