from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Contraseña', 
                                    validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Rol', choices=[('student', 'Estudiante'), ('teacher', 'Docente')], 
                      validators=[DataRequired()])
    submit = SubmitField('Registrarse')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Este usuario ya existe. Por favor elige otro.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este email ya está registrado.')


class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')


class ActivityForm(FlaskForm):
    title = StringField('Título de la Actividad', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Descripción')
    difficulty = SelectField('Dificultad', 
                            choices=[('easy', 'Fácil'), ('medium', 'Medio'), ('hard', 'Difícil')],
                            validators=[DataRequired()])
    subject = StringField('Materia', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Crear Actividad')


class QuestionForm(FlaskForm):
    question_text = TextAreaField('Pregunta', validators=[DataRequired()])
    option_a = StringField('Opción A', validators=[DataRequired(), Length(max=200)])
    option_b = StringField('Opción B', validators=[DataRequired(), Length(max=200)])
    option_c = StringField('Opción C', validators=[DataRequired(), Length(max=200)])
    option_d = StringField('Opción D', validators=[DataRequired(), Length(max=200)])
    correct_answer = RadioField('Respuesta Correcta', 
                               choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')],
                               validators=[DataRequired()])
    points = SelectField('Puntos', choices=[(1, '1'), (2, '2'), (3, '3'), (5, '5')], 
                        coerce=int, validators=[DataRequired()])
    submit = SubmitField('Agregar Pregunta')