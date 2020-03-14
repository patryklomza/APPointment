from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from datetime import datetime, date
from app.models import Visit, ScheduleTime, Court


class VisitForm(FlaskForm):
    visit_date = DateField('Data nowej wizyty',render_kw={"type":"date"},
                           validators=[DataRequired(message='Podaj datę!')])
    visit_time = QuerySelectField('Godzina nowej wizyty:', query_factory=lambda: ScheduleTime.query, allow_blank=False)
    submit = SubmitField('Wyślij')

    def validate_visit_date(self, visit_date):
        if visit_date.data < date.today():
            raise ValidationError('Podany termin jest z przeszłości!')

    def validate_visit_time(self, visit_time):
        available_courts = Court.get_available_courts(date=self.visit_date.data, time=self.visit_time.data.time)
        date_and_time = Visit.query.filter_by(visit_date=self.visit_date.data, visit_time=visit_time.data.time).first()
        if date_and_time is not None and available_courts is None:
            raise ValidationError('Wszystkie korty są już zarezerwowane!!!')




