from flask_wtf import FlaskForm
from wtforms import StringField,  PasswordField, BooleanField, SubmitField, DateField, TimeField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired(message="Pole wymagane")])
    password = PasswordField('Hasło', validators=[DataRequired(message="Pole wymagane")])
    remember_me = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj')


class VisitForm(FlaskForm):
    visit_date = DateField('Data nowej wizyty',render_kw={"type":"date"})
    visit_time = TimeField('Godzina nowej wizyty',render_kw={"type":"time"})
    submit = SubmitField('Wyślij')


class RegistrationForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired(message="Pole wymagane")])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Hasło użytkownika', validators=[DataRequired()])
    password2 = PasswordField('Potwierdź hasło', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Zarejestruj')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Podana nazwa użytkownika jest już zajęta.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('Podany adres e-mail został już wykorzystany podczas rejestracji.')
