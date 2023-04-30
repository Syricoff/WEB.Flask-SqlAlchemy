from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField
from wtforms import BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired


class DepartmentForm(FlaskForm):
    title = StringField('Вид департамента', validators=[DataRequired()])
    chief = IntegerField("Глава департамента", validators=[DataRequired()])
    members = StringField('Участники', validators=[DataRequired("Пример: '1, 2' ")])
    email = EmailField('Почта', validators=[DataRequired()])
    submit = SubmitField('Применить')