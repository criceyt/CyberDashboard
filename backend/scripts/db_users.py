import sys
import os

# Añadir el directorio backend al sys.path para que Python encuentre 'models' y 'app'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import db, User
from app import create_app

app = create_app()

with app.app_context():
    # Crear usuario admin con contraseña hasheada
    user = User(username='admin')
    user.set_password('admin123')
    db.session.add(user)
    db.session.commit()

    print("Usuario admin creado o actualizado correctamente.")
