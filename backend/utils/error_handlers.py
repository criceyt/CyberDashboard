from flask import jsonify
from flask_jwt_extended import JWTManager

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Solicitud incorrecta (400)"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Recurso no encontrado (404)"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Error interno del servidor (500)"}), 500

def register_jwt_error_handlers(app, jwt: JWTManager):
    @jwt.unauthorized_loader
    def unauthorized_callback(reason):
        return jsonify({"error": "No se proporcionó token JWT válido", "details": reason}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        return jsonify({"error": "Token JWT inválido", "details": reason}), 422

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"error": "Token JWT expirado"}), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({"error": "Token JWT revocado"}), 401
