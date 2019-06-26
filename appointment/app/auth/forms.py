from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired(message="Pole wymagane")])
    email = StringField('E-mail', validators=[DataRequired(), Email(message='Niepoprawny format adresu!')])
    password = PasswordField('Hasło użytkownika', validators=[DataRequired()])
    password2 = PasswordField('Potwierdź hasło', validators=[DataRequired(), EqualTo('password', message='Podaj identyczne hasła!')])
    submit = SubmitField('Zarejestruj')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Podana nazwa użytkownika jest już zajęta.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('Podany adres e-mail został już wykorzystany podczas rejestracji.')


class LoginForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired(message="Pole wymagane")])
    password = PasswordField('Hasło', validators=[DataRequired(message="Pole wymagane")])
    remember_me = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj')