from flask_wtf import FlaskForm
from wtforms import StringField,  PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired(message="Pole wymagane")])
    password = PasswordField('Hasło', validators=[DataRequired(message="Pole wymagane")])
    remember_me = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj')