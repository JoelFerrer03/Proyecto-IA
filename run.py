from app import create_app, db
from app.models import User, Activity, Question, Result

app = create_app()

# Crear las tablas si no existen
with app.app_context():
    db.create_all()
    print("Base de datos inicializada correctamente")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)