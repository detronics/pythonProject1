from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import Length, DataRequired, EqualTo


class LoginForm(FlaskForm):
    login = StringField(' Логин: ', validators=[DataRequired()])
    password = PasswordField('Пароль: ', validators=[DataRequired(), Length(min=4)])
    remember_me = BooleanField('Запомнить меня', default=False)
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    login = StringField(' Логин: ', validators=[DataRequired(), Length(min=2, message='Логин должен быть более двух символов')])
    psw1 = PasswordField('Пароль: ', validators=[DataRequired(), Length(min=4, message='Пароль должен быть более четырех символов')])
    psw2 = PasswordField('Повторите пароль: ', validators=[DataRequired(), EqualTo(psw1, message='Пароли не совпадают')])
    name = StringField('Имя:', validators=[DataRequired()])
    subname = StringField('Фамилия: ', validators=[DataRequired()])
    cognomen = StringField('Отчество: ', validators=[DataRequired()])
    age = StringField('Возраст: ', validators=[DataRequired()])
    weight = StringField('Вес: ', validators=[DataRequired()])
    height = StringField('Рост: ', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')