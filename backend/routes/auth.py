from flask import Blueprint, request, jsonify
from models import User
from werkzeug.security import check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=username)
        return jsonify({
            'message': 'Login correcto',
            'access_token': access_token
        }), 200
    else:
        return jsonify({'error': 'Contraseña incorrecta'}), 401


@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    """
    Ruta protegida que requiere un access_token válido
    """
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Endpoint para renovar el access_token usando un refresh_token
    """
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200
