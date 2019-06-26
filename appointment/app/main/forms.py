from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, SelectField
from wtforms.validators import DataRequired


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

    visit_date = DateField('Data nowej wizyty',render_kw={"type":"date"},
                           validators=[DataRequired(message='Podaj datę!')])
    visit_time = SelectField('Godzina nowej wizyty', choices=choices)
    submit = SubmitField('Wyślij')
