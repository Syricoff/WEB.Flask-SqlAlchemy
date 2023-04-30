from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, IntegerField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта/Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    age = IntegerField("Возраст пользователя", validators=[DataRequired()])
    position = StringField('Позиция пользователя', validators=[DataRequired()])
    speciality = StringField('Специальность пользователя', validators=[DataRequired()])
    address = StringField('Адрес пользователя', validators=[DataRequired()])
    submit = SubmitField('Войти')