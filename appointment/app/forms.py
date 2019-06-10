from flask_wtf import FlaskForm
from wtforms import StringField,  PasswordField, BooleanField, SubmitField, DateField, TimeField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired(message="Pole wymagane")])
    password = PasswordField('Hasło', validators=[DataRequired(message="Pole wymagane")])
    remember_me = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj')


class VisitForm(FlaskForm):
    visit_date = DateField('Data nowej wizyty',render_kw={"type":"date"})
    visit_time = TimeField('Godzina nowej wizyty',render_kw={"type":"time"})
    submit = SubmitField('Wyślij')