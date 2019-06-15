from flask_wtf import FlaskForm
from wtforms import StringField,  PasswordField, BooleanField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired(message="Pole wymagane")])
    password = PasswordField('Hasło', validators=[DataRequired(message="Pole wymagane")])
    remember_me = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj')


class VisitForm(FlaskForm):
    choices = [('08:00', '08:00'), ('08:30', '08:30'),
               ('09:00', '09:00'), ('09:30', '09:30'),
               ('10:00', '10:00'), ('10:30', '10:30'),
               ('11:00', '11:00'), ('11:00', '11:00'),
               ('12:00', '12:00'), ('12:30', '12:30'),
               ('13:00', '13:00'), ('13:30', '13:30'),
               ('14:00', '14:00'), ('14:30', '14:30'),
               ('15:00', '15:00'), ('15:30', '15:30'),
               ('16:00', '16:00'), ('16:30', '16:30'),
               ('17:00', '17:00'), ('17:30', '17:30'),
               ('18:00', '18:00'), ('18:30', '18:30')]

    visit_date = DateField('Data nowej wizyty',render_kw={"type":"date"})
   # visit_time = TimeField('Godzina nowej wizyty',render_kw={"type":"time"})
    visit_time = SelectField('Godzina nowej wizyty', choices=choices)
    submit = SubmitField('Wyślij')


class RegistrationForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired(message="Pole wymagane")])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Hasło użytkownika', validators=[DataRequired()])
    password2 = PasswordField('Potwierdź hasło', validators=[DataRequired(), EqualTo('password',message='Podaj identyczne hasła!')])
    submit = SubmitField('Zarejestruj')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Podana nazwa użytkownika jest już zajęta.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('Podany adres e-mail został już wykorzystany podczas rejestracji.')
