import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Crear tablas
    db.create_all()

    # Verificar si ya existe un admin
    admin = User.query.filter_by(username='admin').first()

    if not admin:
        admin = User(
            username='admin',
            email='admin@eduplatform.com',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('�o. Usuario administrador creado')
    else:
        print('�s���? El usuario admin ya existe')

    print('\nCredenciales del administrador:')
    print('  Usuario: admin')
    print('  Contrase�a: admin123')
