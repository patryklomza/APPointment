from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, ValidationError

from app.models import Visit


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

    def validate_visit_time(self, visit_time):
        date_and_time = Visit.query.filter_by(visit_date=self.visit_date.data,
                                              visit_time=visit_time.data).first()
        if date_and_time is not None:
            raise ValidationError('Podany termin jest już zajęty.')
