from flask import render_template, redirect, url_for, flash, request, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Activity, Question, Result
from app.forms import RegistrationForm, LoginForm, ActivityForm, QuestionForm
from app.logic import LogicEngine
from datetime import datetime
from functools import wraps

# Decorador para verificar roles
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                flash('No tienes permisos para acceder a esta página', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def init_routes(app):
    
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            if current_user.role == 'student':
                return redirect(url_for('student_dashboard'))
            elif current_user.role == 'teacher':
                return redirect(url_for('teacher_dashboard'))
            elif current_user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
        return render_template('index.html')
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(
                username=form.username.data,
                email=form.email.data,
                role=form.role.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            
            flash(f'Cuenta creada exitosamente para {form.username.data}!', 'success')
            return redirect(url_for('login'))
        
        return render_template('register.html', form=form)
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            
            if user and user.check_password(form.password.data):
                login_user(user)
                flash(f'Bienvenido {user.username}!', 'success')
                
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                
                if user.role == 'student':
                    return redirect(url_for('student_dashboard'))
                elif user.role == 'teacher':
                    return redirect(url_for('teacher_dashboard'))
                else:
                    return redirect(url_for('admin_dashboard'))
            else:
                flash('Usuario o contraseña incorrectos', 'danger')
        
        return render_template('login.html', form=form)
    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Has cerrado sesión correctamente', 'info')
        return redirect(url_for('index'))
    
    # ==================== RUTAS DE ESTUDIANTE ====================
    
    @app.route('/student/dashboard')
    @login_required
    @role_required('student')
    def student_dashboard():
        activities = Activity.query.filter_by(is_active=True).all()
        
        # Obtener resultados del estudiante
        my_results = Result.query.filter_by(student_id=current_user.id).all()
        completed_activity_ids = set(r.activity_id for r in my_results)
        
        # Calcular estadísticas
        average = LogicEngine.calculate_student_average(current_user.id)
        performance_level = LogicEngine.get_student_performance_level(current_user.id)
        recommendations = LogicEngine.get_recommendations(current_user.id)
        suggested_difficulty = LogicEngine.adjust_difficulty(current_user.id)
        
        return render_template('student_dashboard.html',
                             activities=activities,
                             completed_ids=completed_activity_ids,
                             average=round(average, 2),
                             performance_level=performance_level,
                             recommendations=recommendations,
                             suggested_difficulty=suggested_difficulty,
                             total_completed=len(my_results))
    
    @app.route('/student/activity/<int:activity_id>', methods=['GET', 'POST'])
    @login_required
    @role_required('student')
    def student_activity(activity_id):
        activity = Activity.query.get_or_404(activity_id)
        
        if request.method == 'POST':
            # Procesar respuestas
            score = 0
            max_score = 0
            start_time = session.get('activity_start_time', datetime.utcnow().timestamp())
            
            for question in activity.questions:
                max_score += question.points
                answer = request.form.get(f'question_{question.id}')
                if answer and answer.lower() == question.correct_answer.lower():
                    score += question.points
            
            # Calcular tiempo
            time_spent = int(datetime.utcnow().timestamp() - start_time)
            percentage = (score / max_score * 100) if max_score > 0 else 0
            
            # Guardar resultado
            result = Result(
                student_id=current_user.id,
                activity_id=activity_id,
                score=score,
                max_score=max_score,
                percentage=percentage,
                time_spent=time_spent
            )
            db.session.add(result)
            db.session.commit()
            
            flash(f'Actividad completada! Obtuviste {score}/{max_score} puntos ({percentage:.1f}%)', 'success')
            return redirect(url_for('student_dashboard'))
        
        # Guardar tiempo de inicio
        session['activity_start_time'] = datetime.utcnow().timestamp()
        
        return render_template('student_activity.html', activity=activity)
    
    # ==================== RUTAS DE DOCENTE ====================
    
    @app.route('/teacher/dashboard')
    @login_required
    @role_required('teacher')
    def teacher_dashboard():
        activities = Activity.query.filter_by(teacher_id=current_user.id).all()
        overview = LogicEngine.get_teacher_overview(current_user.id)
        struggling_students = LogicEngine.detect_struggling_students(current_user.id)
        
        return render_template('teacher_dashboard.html',
                             activities=activities,
                             overview=overview,
                             struggling_students=struggling_students)
    
    @app.route('/teacher/create_activity', methods=['GET', 'POST'])
    @login_required
    @role_required('teacher')
    def create_activity():
        form = ActivityForm()
        
        if form.validate_on_submit():
            activity = Activity(
                title=form.title.data,
                description=form.description.data,
                difficulty=form.difficulty.data,
                subject=form.subject.data,
                teacher_id=current_user.id
            )
            db.session.add(activity)
            db.session.commit()
            
            flash(f'Actividad "{activity.title}" creada exitosamente!', 'success')
            return redirect(url_for('add_questions', activity_id=activity.id))
        
        return render_template('create_activity.html', form=form)
    
    @app.route('/teacher/activity/<int:activity_id>/add_questions', methods=['GET', 'POST'])
    @login_required
    @role_required('teacher')
    def add_questions(activity_id):
        activity = Activity.query.get_or_404(activity_id)
        
        if activity.teacher_id != current_user.id:
            flash('No tienes permisos para editar esta actividad', 'danger')
            return redirect(url_for('teacher_dashboard'))
        
        form = QuestionForm()
        
        if form.validate_on_submit():
            question = Question(
                activity_id=activity_id,
                question_text=form.question_text.data,
                option_a=form.option_a.data,
                option_b=form.option_b.data,
                option_c=form.option_c.data,
                option_d=form.option_d.data,
                correct_answer=form.correct_answer.data,
                points=form.points.data
            )
            db.session.add(question)
            db.session.commit()
            
            flash('Pregunta agregada exitosamente!', 'success')
            
            if request.form.get('add_another'):
                return redirect(url_for('add_questions', activity_id=activity_id))
            else:
                return redirect(url_for('teacher_dashboard'))
        
        return render_template('add_questions.html', form=form, activity=activity)
    
    @app.route('/teacher/students')
    @login_required
    @role_required('teacher')
    def view_students():
        # Obtener estudiantes que han hecho actividades del docente
        activities = Activity.query.filter_by(teacher_id=current_user.id).all()
        activity_ids = [a.id for a in activities]
        
        students_data = []
        students = db.session.query(User).join(Result).filter(
            Result.activity_id.in_(activity_ids),
            User.role == 'student'
        ).distinct().all()
        
        for student in students:
            avg = LogicEngine.calculate_student_average(student.id)
            results = Result.query.filter_by(student_id=student.id).filter(
                Result.activity_id.in_(activity_ids)
            ).all()
            
            students_data.append({
                'student': student,
                'average': round(avg, 2),
                'total_activities': len(results),
                'performance': LogicEngine.get_student_performance_level(student.id)
            })
        
        return render_template('view_students.html', students_data=students_data)
    
    @app.route('/teacher/activity/<int:activity_id>/stats')
    @login_required
    @role_required('teacher')
    def activity_stats(activity_id):
        activity = Activity.query.get_or_404(activity_id)
        
        if activity.teacher_id != current_user.id:
            flash('No tienes permisos para ver esta actividad', 'danger')
            return redirect(url_for('teacher_dashboard'))
        
        stats = LogicEngine.get_activity_stats(activity_id)
        results = Result.query.filter_by(activity_id=activity_id).all()
        
        return render_template('activity_stats.html', 
                             activity=activity, 
                             stats=stats,
                             results=results)
    
    # ==================== RUTAS DE ADMINISTRADOR ====================
    
    @app.route('/admin/dashboard')
    @login_required
    @role_required('admin')
    def admin_dashboard():
        total_users = User.query.count()
        total_students = User.query.filter_by(role='student').count()
        total_teachers = User.query.filter_by(role='teacher').count()
        total_activities = Activity.query.count()
        
        recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
        
        return render_template('admin_dashboard.html',
                             total_users=total_users,
                             total_students=total_students,
                             total_teachers=total_teachers,
                             total_activities=total_activities,
                             recent_users=recent_users)
    
    @app.route('/admin/users')
    @login_required
    @role_required('admin')
    def manage_users():
        users = User.query.all()
        return render_template('manage_users.html', users=users)
    
    @app.route('/admin/user/<int:user_id>/delete', methods=['POST'])
    @login_required
    @role_required('admin')
    def delete_user(user_id):
        user = User.query.get_or_404(user_id)
        
        if user.id == current_user.id:
            flash('No puedes eliminar tu propia cuenta', 'danger')
            return redirect(url_for('manage_users'))
        
        db.session.delete(user)
        db.session.commit()
        flash(f'Usuario {user.username} eliminado correctamente', 'success')
        return redirect(url_for('manage_users'))

# Inicializar rutas
from flask import current_app
with current_app.app_context():
    init_routes(current_app)