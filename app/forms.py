from flask_wtf import FlaskForm

import wtforms as wf

from . import app
from .models import Position

a = '1', '2'


def get_positiones():
    with app.app_context():
        positionies = Position.query.all()
        choices = []
        for position in positionies:
            choices.append((position.id, position.name))
        return choices


class PositionForm(FlaskForm):
    name = wf.StringField(label='Должность', validators=[
        wf.validators.DataRequired()
    ])
    department = wf.StringField(label='Отдел')
    wage = wf.IntegerField(label='Заработная плата', validators=[
        wf.validators.DataRequired()
    ])

    def validate_wage(self, field):
        if field.data <= 0:
            raise wf.validators.ValidationError('не может быть ниже 0')


class EmployeeForm(FlaskForm):
    name = wf.StringField(label='ФИО', validators=[
        wf.validators.DataRequired()
    ])
    inn = wf.StringField(label='ИНН', validators=[
        wf.validators.Length(min=14, max=14),
        wf.validators.DataRequired()
    ])
    position_id = wf.SelectField(label='Должность', choices=[], validators=[
        wf.validators.DataRequired()
    ])


    def validate_inn(self, field):
        if not field.data[:1].startswith(a):
            raise wf.validators.ValidationError('должно начинаться с 1 или 2')

    # def validate_inn(self, field):
    #     if not field.data[0] == '1' or field.data[0] == '2':
    #         raise wf.validators.ValidationError('ИНН начинается с 1 или 2!')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.position_id.choices = get_positiones()


class UserForm(FlaskForm):
    username = wf.StringField(label='Логин пользователя', validators=[
        wf.validators.DataRequired(),
        wf.validators.Length(min=8, max=24)
    ])
    password = wf.PasswordField(label='Пароль', validators=[
        wf.validators.DataRequired()
    ])

    def validate_password(self, field):
        if field.data.isdigit() or field.data.isalpha():
            raise wf.validators.ValidationError('Пароль должен содержать числа и буквы')
