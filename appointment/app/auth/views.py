from app import db
from .forms import LoginForm, RegistrationForm
from app.models import User
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from . import auth


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Display registration form and send back provided data

    If user is already logged in redirect to index endpoint
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Gratulacje! Zostałeś poprawnie zarejestrowany!', category='success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Rejestracja', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Display user login form

    When user is already logged in, redirect to index endpoint.
    If username and password are correct login_user() sets current_user
    variable to that user
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Nieprawidłowa nazwa użytkownika lub hasło!', category='danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    flash('Wylogowano poprawnie', category='success')
    return redirect(url_for('main.index'))
