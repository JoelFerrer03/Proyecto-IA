from app.models import Result, Activity, User
from app import db
from sqlalchemy import func

class LogicEngine:
    """Motor de lógica para recomendaciones y análisis"""
    
    @staticmethod
    def calculate_student_average(student_id):
        """Calcula el promedio general del estudiante"""
        results = Result.query.filter_by(student_id=student_id).all()
        if not results:
            return 0
        return sum(r.percentage for r in results) / len(results)
    
    @staticmethod
    def get_student_performance_level(student_id):
        """Determina el nivel de rendimiento del estudiante"""
        avg = LogicEngine.calculate_student_average(student_id)
        if avg >= 80:
            return 'excelente'
        elif avg >= 60:
            return 'bueno'
        elif avg >= 40:
            return 'regular'
        else:
            return 'bajo'
    
    @staticmethod
    def get_recommendations(student_id):
        """Genera recomendaciones basadas en el rendimiento"""
        results = Result.query.filter_by(student_id=student_id).order_by(Result.completed_at.desc()).limit(5).all()
        
        if not results:
            return ["Completa tu primera actividad para recibir recomendaciones personalizadas"]
        
        avg = sum(r.percentage for r in results) / len(results)
        recommendations = []
        
        # Lógica de recomendaciones
        if avg < 50:
            recommendations.append("📚 Tu rendimiento necesita mejorar. Revisa los temas básicos.")
            recommendations.append("💡 Dedica más tiempo a practicar ejercicios simples.")
            recommendations.append("👨‍🏫 Considera pedir ayuda a tu docente.")
        elif avg < 70:
            recommendations.append("📈 Vas por buen camino. Sigue practicando regularmente.")
            recommendations.append("🎯 Enfócate en los temas donde has tenido más errores.")
        else:
            recommendations.append("🌟 ¡Excelente trabajo! Sigue así.")
            recommendations.append("🚀 Prueba con actividades de mayor dificultad.")
        
        # Analizar tiempo de respuesta
        avg_time = sum(r.time_spent for r in results if r.time_spent) / len([r for r in results if r.time_spent]) if any(r.time_spent for r in results) else 0
        if avg_time > 600:  # Más de 10 minutos
            recommendations.append("⏱️ Intenta gestionar mejor tu tiempo en las actividades.")
        
        return recommendations
    
    @staticmethod
    def adjust_difficulty(student_id):
        """Ajusta la dificultad recomendada según últimos intentos"""
        recent_results = Result.query.filter_by(student_id=student_id).order_by(Result.completed_at.desc()).limit(3).all()
        
        if not recent_results:
            return 'easy'
        
        avg = sum(r.percentage for r in recent_results) / len(recent_results)
        
        if avg >= 85:
            return 'hard'
        elif avg >= 60:
            return 'medium'
        else:
            return 'easy'
    
    @staticmethod
    def detect_struggling_students(teacher_id):
        """Detecta estudiantes con bajo rendimiento"""
        activities = Activity.query.filter_by(teacher_id=teacher_id).all()
        activity_ids = [a.id for a in activities]
        
        struggling = []
        
        # Obtener todos los estudiantes que han hecho actividades de este docente
        students = db.session.query(User).join(Result).filter(
            Result.activity_id.in_(activity_ids),
            User.role == 'student'
        ).distinct().all()
        
        for student in students:
            avg = LogicEngine.calculate_student_average(student.id)
            if avg < 60:
                struggling.append({
                    'student': student,
                    'average': round(avg, 2),
                    'status': 'Necesita apoyo'
                })
        
        return struggling
    
    @staticmethod
    def get_activity_stats(activity_id):
        """Obtiene estadísticas de una actividad"""
        results = Result.query.filter_by(activity_id=activity_id).all()
        
        if not results:
            return {
                'total_attempts': 0,
                'average_score': 0,
                'pass_rate': 0,
                'avg_time': 0
            }
        
        total = len(results)
        passed = len([r for r in results if r.percentage >= 60])
        
        return {
            'total_attempts': total,
            'average_score': round(sum(r.percentage for r in results) / total, 2),
            'pass_rate': round((passed / total) * 100, 2),
            'avg_time': round(sum(r.time_spent for r in results if r.time_spent) / len([r for r in results if r.time_spent]), 2) if any(r.time_spent for r in results) else 0
        }
    
    @staticmethod
    def get_teacher_overview(teacher_id):
        """Resumen general para el docente"""
        activities = Activity.query.filter_by(teacher_id=teacher_id).all()
        
        total_activities = len(activities)
        total_results = sum(len(a.results) for a in activities)
        
        if total_results == 0:
            return {
                'total_activities': total_activities,
                'total_students': 0,
                'average_performance': 0,
                'alerts': 0
            }
        
        all_percentages = [r.percentage for a in activities for r in a.results]
        students = set(r.student_id for a in activities for r in a.results)
        alerts = len(LogicEngine.detect_struggling_students(teacher_id))
        
        return {
            'total_activities': total_activities,
            'total_students': len(students),
            'average_performance': round(sum(all_percentages) / len(all_percentages), 2),
            'alerts': alerts
        }