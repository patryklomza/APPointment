from app import app, db
from app.forms import LoginForm, VisitForm, RegistrationForm
from app.models import User, Visit
from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Gratulacje! Zostałeś poprawnie zarejestrowany!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Rejestracja', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('Wylogowano poprawnie')
    return redirect(url_for('index'))


@app.route('/visit', methods=['GET','POST'])
@login_required
def visit():
    form = VisitForm()
    if form.validate_on_submit():
        visit = Visit(visit_date=str(form.visit_date.data),
                      visit_time=str(form.visit_time.data),
                      customer=current_user)
        db.session.add(visit)
        db.session.commit()
        flash(f'Wizyta umówiona {form.visit_date.data} na godzinę: {form.visit_time.data}.')
        return redirect(url_for('index'))
    return render_template('visit.html', title='Umów wizytę', form=form)
