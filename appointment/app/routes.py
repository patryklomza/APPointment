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
        flash('Gratulacje! Zostałeś poprawnie zarejestrowany!', category='success')
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
            flash('Nieprawidłowa nazwa użytkownika lub hasło!', category='danger')
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
    flash('Wylogowano poprawnie', category='success')
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
        flash(f'Wizyta umówiona {form.visit_date.data} na godzinę: {form.visit_time.data}.', category='success')
        return redirect(url_for('user', username=current_user.username))
    return render_template('visit.html', title='Umów wizytę', form=form)


@app.route('/user/visits/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user != current_user:
        flash('Brak dostępu!', category='warning')
        return redirect(url_for('user', username=current_user.username))
    if user.is_admin:
        visits = Visit.query.all()
    else:
        visits = Visit.query.filter_by(user_id=user.id)
    return render_template('user.html', user=user, visits=visits)


@app.route('/user/visits/delete/<visit>')
@login_required
def delete_visit(visit):
    visit_to_delete = Visit.query.filter_by(id=visit).first_or_404()
    user = User.query.filter_by(id=visit_to_delete.user_id).first_or_404()
    if user != current_user:
        flash('Brak autoryzacji!', category='warning')
        return redirect(url_for('user', username=current_user.username))
    db.session.delete(visit_to_delete)
    db.session.commit()
    flash('Anulowano wizytę', category='success')
    return redirect(url_for('user', username=current_user.username))
