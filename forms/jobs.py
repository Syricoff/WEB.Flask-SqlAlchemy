from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    team_leader = IntegerField("id Главный", validators=[DataRequired()])
    job = StringField('Вид работы', validators=[DataRequired()])
    work_size = IntegerField("Время работы", validators=[DataRequired()])
    collaborators = StringField('Участники', validators=[DataRequired("Пример: '1, 2' ")])
    is_finished = BooleanField('Работа завершена?')
    submit = SubmitField('Применить')
