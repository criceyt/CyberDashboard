from .scan import scan_bp
from .os_scan import os_scan_bp

def register_routes(app):
    app.register_blueprint(scan_bp, url_prefix='/api')
    app.register_blueprint(os_scan_bp, url_prefix='/api')
