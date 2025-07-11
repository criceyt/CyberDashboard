import os
from flask import Flask
from flasgger import Swagger
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from routes.scan import scan_bp
from routes.os_scan import os_scan_bp
from routes.dir_enum import dir_enum_bp
from routes.vuln_scan import vuln_scan_bp
from utils.error_handlers import register_error_handlers, register_jwt_error_handlers
from utils.logger import setup_logger
from models import db
from routes.celery_worker import init_celery
from routes.auth import auth_bp



def create_app():
    app = Flask(__name__)

    # Configuración desde config.py
    app.config.from_object('config.Config')

    # Inicializar extensiones
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)  # 👈 JWT habilitado

    # Inicializar Celery
    init_celery(app)

    # Registrar Blueprints
    app.register_blueprint(scan_bp, url_prefix='/api')
    app.register_blueprint(auth_bp)  # 👈 Endpoints de login
    app.register_blueprint(os_scan_bp, url_prefix='/api')
    app.register_blueprint(dir_enum_bp, url_prefix='/api')
    app.register_blueprint(vuln_scan_bp)

    # Registrar manejadores de errores y logger
    register_error_handlers(app)
    register_jwt_error_handlers(app, jwt)  # 👈 Errores específicos de JWT
    setup_logger()

    # Documentación Swagger
    Swagger(app)

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
