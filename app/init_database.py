import sys
from pathlib import Path

# Permite ejecutar el script directamente (python app/init_database.py).
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app import create_app, db
from app.models import User, Activity, Question, Result

app = create_app()

with app.app_context():
    print("🔄 Eliminando base de datos anterior...")
    db.drop_all()
    
    print("🔄 Creando nuevas tablas...")
    db.create_all()
    
    print("👤 Creando usuarios de prueba...")
    
    # Crear administrador
    admin = User(
        username='admin',
        email='admin@eduplatform.com',
        role='admin'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    
    # Crear docentes
    teacher1 = User(
        username='profesor1',
        email='profesor1@eduplatform.com',
        role='teacher'
    )
    teacher1.set_password('profesor123')
    db.session.add(teacher1)
    
    teacher2 = User(
        username='maria_lopez',
        email='maria@eduplatform.com',
        role='teacher'
    )
    teacher2.set_password('maria123')
    db.session.add(teacher2)
    
    # Crear estudiantes
    students_data = [
        ('juan_perez', 'juan@eduplatform.com', 'juan123'),
        ('ana_garcia', 'ana@eduplatform.com', 'ana123'),
        ('carlos_rodriguez', 'carlos@eduplatform.com', 'carlos123'),
        ('lucia_martinez', 'lucia@eduplatform.com', 'lucia123'),
        ('pedro_sanchez', 'pedro@eduplatform.com', 'pedro123'),
    ]
    
    students = []
    for username, email, password in students_data:
        student = User(username=username, email=email, role='student')
        student.set_password(password)
        db.session.add(student)
        students.append(student)
    
    db.session.commit()
    print(f"✅ Creados {len(students)} estudiantes")
    
    # Crear actividades
    print("📋 Creando actividades de prueba...")
    
    # Actividad 1: Matemáticas Básicas
    activity1 = Activity(
        title='Álgebra Básica - Ecuaciones Lineales',
        description='Evaluación sobre conceptos fundamentales de ecuaciones lineales y su resolución',
        difficulty='easy',
        subject='Matemáticas',
        teacher_id=teacher1.id
    )
    db.session.add(activity1)
    db.session.commit()
    
    # Preguntas para Actividad 1
    questions_math = [
        {
            'text': '¿Cuál es el valor de x en la ecuación: 2x + 5 = 13?',
            'a': 'x = 3', 'b': 'x = 4', 'c': 'x = 5', 'd': 'x = 6',
            'correct': 'b', 'points': 2
        },
        {
            'text': 'Si 3x - 7 = 14, ¿cuál es el valor de x?',
            'a': 'x = 5', 'b': 'x = 6', 'c': 'x = 7', 'd': 'x = 8',
            'correct': 'c', 'points': 2
        },
        {
            'text': '¿Qué operación debes realizar primero para resolver: 5x + 3 = 18?',
            'a': 'Sumar 3', 'b': 'Restar 3', 'c': 'Multiplicar por 5', 'd': 'Dividir por 5',
            'correct': 'b', 'points': 1
        },
        {
            'text': '¿Cuál es la pendiente de la recta y = 3x + 2?',
            'a': '2', 'b': '3', 'c': '5', 'd': '1',
            'correct': 'b', 'points': 2
        }
    ]
    
    for q_data in questions_math:
        question = Question(
            activity_id=activity1.id,
            question_text=q_data['text'],
            option_a=q_data['a'],
            option_b=q_data['b'],
            option_c=q_data['c'],
            option_d=q_data['d'],
            correct_answer=q_data['correct'],
            points=q_data['points']
        )
        db.session.add(question)
    
    # Actividad 2: Historia
    activity2 = Activity(
        title='Revolución Industrial',
        description='Evaluación sobre los acontecimientos más importantes de la Revolución Industrial',
        difficulty='medium',
        subject='Historia',
        teacher_id=teacher1.id
    )
    db.session.add(activity2)
    db.session.commit()
    
    questions_history = [
        {
            'text': '¿En qué siglo comenzó la Revolución Industrial?',
            'a': 'Siglo XVI', 'b': 'Siglo XVII', 'c': 'Siglo XVIII', 'd': 'Siglo XIX',
            'correct': 'c', 'points': 1
        },
        {
            'text': '¿Qué país fue el primero en experimentar la Revolución Industrial?',
            'a': 'Francia', 'b': 'Alemania', 'c': 'Estados Unidos', 'd': 'Inglaterra',
            'correct': 'd', 'points': 2
        },
        {
            'text': '¿Cuál fue uno de los inventos más importantes de esta época?',
            'a': 'El teléfono', 'b': 'La máquina de vapor', 'c': 'El automóvil', 'd': 'La computadora',
            'correct': 'b', 'points': 2
        }
    ]
    
    for q_data in questions_history:
        question = Question(
            activity_id=activity2.id,
            question_text=q_data['text'],
            option_a=q_data['a'],
            option_b=q_data['b'],
            option_c=q_data['c'],
            option_d=q_data['d'],
            correct_answer=q_data['correct'],
            points=q_data['points']
        )
        db.session.add(question)
    
    # Actividad 3: Ciencias
    activity3 = Activity(
        title='Fotosíntesis y Respiración Celular',
        description='Conceptos básicos de procesos biológicos en las plantas',
        difficulty='medium',
        subject='Biología',
        teacher_id=teacher2.id
    )
    db.session.add(activity3)
    db.session.commit()
    
    questions_science = [
        {
            'text': '¿Qué gas liberan las plantas durante la fotosíntesis?',
            'a': 'Dióxido de carbono', 'b': 'Oxígeno', 'c': 'Nitrógeno', 'd': 'Hidrógeno',
            'correct': 'b', 'points': 2
        },
        {
            'text': '¿En qué parte de la célula vegetal ocurre la fotosíntesis?',
            'a': 'Núcleo', 'b': 'Mitocondria', 'c': 'Cloroplasto', 'd': 'Ribosoma',
            'correct': 'c', 'points': 2
        },
        {
            'text': '¿Qué necesitan las plantas para realizar la fotosíntesis?',
            'a': 'Solo agua', 'b': 'Solo luz solar', 'c': 'Luz solar, agua y CO2', 'd': 'Solo CO2',
            'correct': 'c', 'points': 3
        }
    ]
    
    for q_data in questions_science:
        question = Question(
            activity_id=activity3.id,
            question_text=q_data['text'],
            option_a=q_data['a'],
            option_b=q_data['b'],
            option_c=q_data['c'],
            option_d=q_data['d'],
            correct_answer=q_data['correct'],
            points=q_data['points']
        )
        db.session.add(question)
    
    # Actividad 4: Programación
    activity4 = Activity(
        title='Introducción a Python',
        description='Conceptos básicos de programación en Python',
        difficulty='hard',
        subject='Programación',
        teacher_id=teacher2.id
    )
    db.session.add(activity4)
    db.session.commit()
    
    questions_programming = [
        {
            'text': '¿Qué estructura de datos es ordenada y mutable en Python?',
            'a': 'Tuple', 'b': 'Set', 'c': 'List', 'd': 'String',
            'correct': 'c', 'points': 2
        },
        {
            'text': '¿Cuál es el operador para exponenciación en Python?',
            'a': '^', 'b': '**', 'c': 'exp()', 'd': 'pow',
            'correct': 'b', 'points': 1
        },
        {
            'text': '¿Qué keyword se usa para definir una función en Python?',
            'a': 'function', 'b': 'func', 'c': 'def', 'd': 'define',
            'correct': 'c', 'points': 1
        },
        {
            'text': '¿Qué método se usa para agregar un elemento al final de una lista?',
            'a': 'add()', 'b': 'append()', 'c': 'insert()', 'd': 'push()',
            'correct': 'b', 'points': 2
        }
    ]
    
    for q_data in questions_programming:
        question = Question(
            activity_id=activity4.id,
            question_text=q_data['text'],
            option_a=q_data['a'],
            option_b=q_data['b'],
            option_c=q_data['c'],
            option_d=q_data['d'],
            correct_answer=q_data['correct'],
            points=q_data['points']
        )
        db.session.add(question)
    
    db.session.commit()
    print("✅ Actividades y preguntas creadas")
    
    # Crear resultados de prueba
    print("📊 Creando resultados de prueba...")
    
    import random
    
    results_data = [
        # Juan - Buen estudiante
        (students[0], activity1, 6, 7, 85.7, 240),
        (students[0], activity2, 4, 5, 80.0, 180),
        (students[0], activity3, 6, 7, 85.7, 200),
        
        # Ana - Estudiante excelente
        (students[1], activity1, 7, 7, 100.0, 200),
        (students[1], activity2, 5, 5, 100.0, 150),
        (students[1], activity3, 7, 7, 100.0, 180),
        (students[1], activity4, 5, 6, 83.3, 300),
        
        # Carlos - Estudiante con dificultades
        (students[2], activity1, 3, 7, 42.9, 400),
        (students[2], activity2, 2, 5, 40.0, 250),
        
        # Lucía - Estudiante promedio
        (students[3], activity1, 5, 7, 71.4, 220),
        (students[3], activity3, 5, 7, 71.4, 210),
        
        # Pedro - Buen estudiante
        (students[4], activity2, 4, 5, 80.0, 190),
        (students[4], activity4, 4, 6, 66.7, 350),
    ]
    
    for student, activity, score, max_score, percentage, time in results_data:
        result = Result(
            student_id=student.id,
            activity_id=activity.id,
            score=score,
            max_score=max_score,
            percentage=percentage,
            time_spent=time
        )
        db.session.add(result)
    
    db.session.commit()
    print("✅ Resultados de prueba creados")
    
    print("\n" + "="*60)
    print("✅ BASE DE DATOS INICIALIZADA CORRECTAMENTE")
    print("="*60)
    print("\n📝 CREDENCIALES DE ACCESO:\n")
    
    print("👨‍💼 ADMINISTRADOR:")
    print("   Usuario: admin")
    print("   Contraseña: admin123\n")
    
    print("👨‍🏫 DOCENTES:")
    print("   Usuario: profesor1 | Contraseña: profesor123")
    print("   Usuario: maria_lopez | Contraseña: maria123\n")
    
    print("🎓 ESTUDIANTES:")
    print("   Usuario: juan_perez | Contraseña: juan123")
    print("   Usuario: ana_garcia | Contraseña: ana123")
    print("   Usuario: carlos_rodriguez | Contraseña: carlos123")
    print("   Usuario: lucia_martinez | Contraseña: lucia123")
    print("   Usuario: pedro_sanchez | Contraseña: pedro123\n")
    
    print("="*60)
    print("🎯 ESTADÍSTICAS:")
    print(f"   • Total usuarios: {User.query.count()}")
    print(f"   • Total actividades: {Activity.query.count()}")
    print(f"   • Total preguntas: {Question.query.count()}")
    print(f"   • Total resultados: {Result.query.count()}")
    print("="*60)
