from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


class User(UserMixin, db.Model):
    """
    Basic User capable of adding new visits and deleting existing ones from his profile.
    is_admin can be set manually to True.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    visits = db.relationship('Visit', backref='customer', lazy='dynamic')
    is_admin = db.Column(db.Boolean(), default=0)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    """Given *id*, returns the associated User object."""
    return User.query.get(int(id))


class Visit(db.Model):
    """
    Visit made by user
    """
    id = db.Column(db.Integer, primary_key=True)
    visit_date = db.Column(db.Text, index=True)
    visit_time = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    time_id = db.Column(db.Integer, db.ForeignKey('default_hour.id'))

    def __repr__(self):
        return f'<Visit {self.date} {self.time}>'


class ScheduleTime(db.Model):
    """
    Default time intervals for making appointments by customers
    """
    __tablename__ = 'default_hour'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Text)
    hours = db.relationship('Visit', backref='hours', lazy='dynamic')

    def __repr__(self):
        return str(self.time)
