from flask import current_app

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin, login_manager
from app import login


class User(UserMixin, db.Model):
    """
    Basic User capable of adding new visits and deleting existing ones from his profile.
    is_admin can be set manually to True.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    visits = db.relationship('Visit', backref='customer', lazy='dynamic')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['APPOINTMENT_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    @property
    def is_administrator(self):
        return self.can(Permission.ADMIN)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    @property
    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login.user_loader
def load_user(id):
    """Given *id*, returns the associated User object."""
    return User.query.get(int(id))


class Visit(db.Model):
    """
    Visit made by user
    """
    __tablename__ = 'visits'
    id = db.Column(db.Integer, primary_key=True)
    visit_date = db.Column(db.Text, index=True)
    visit_time = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    time_id = db.Column(db.Integer, db.ForeignKey('default_hours.id'))
    court_id = db.Column(db.Integer, db.ForeignKey('courts.id'))

    def __repr__(self):
        return f'<Visit {self.date} {self.time}>'

    def assign_court(self, court_list):
            self.court_id = court_list.pop()

class ScheduleTime(db.Model):
    """
    Default time intervals for making appointments by customers
    """
    __tablename__ = 'default_hours'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Text)
    hours = db.relationship('Visit', backref='hours', lazy='dynamic')

    def __repr__(self):
        return str(self.time)


class Court(db.Model):
    __tablename__ = 'courts'
    id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean, default=True)
    visits = db.relationship('Visit', backref='visits', lazy='dynamic')

    def __str__(self):
        return f'court #{self.id}'

    @staticmethod
    def get_active_courts_id_list():
        courts = Court.query.filter_by(is_active=True).all()
        active_courts = [court.id for court in courts]
        return active_courts

    @staticmethod
    def get_reserved_courts_id_list(date, time):
        visits = Visit.query.filter_by(visit_date=date, visit_time=time).all()
        reserved_courts = [visit.court_id for visit in visits]
        return reserved_courts

    @staticmethod
    def get_available_courts(date, time):
        active_courts = Court.get_active_courts_id_list()
        reserved_courts = Court.get_reserved_courts_id_list(date, time)
        available_courts = list(set(active_courts) - set(reserved_courts))
        if available_courts:
            return available_courts
        else:
            return None



class Role(db.Model):
    '''
    Role model
    default field should be true only for one role, and false for others.
    Role marked as default is assigned to new users upon registration.
    '''
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),  unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def __repr__(self):
        return f'<Role {self.name}>'

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.ADD, Permission.EDIT, Permission.DELETE],
            'Employee': [Permission.ADD, Permission.EDIT, Permission.DELETE, Permission.MODERATE],
            'Administrator': [Permission.ADD, Permission.EDIT, Permission.DELETE, Permission.MODERATE, Permission.ADMIN]
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

class Permission:
    ADD = 1
    EDIT = 2
    DELETE = 4
    MODERATE = 8
    ADMIN = 16
