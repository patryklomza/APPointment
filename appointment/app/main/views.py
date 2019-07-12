from app import db
from app.models import User, Visit
from flask import render_template, url_for, flash, redirect
from flask_login import current_user, login_required
from .forms import VisitForm
from . import main


@main.route('/')
@main.route('/index')
def index():
    return render_template('main/index.html', title='Home')


@main.route('/visit', methods=['GET','POST'])
@login_required
def visit():
    """Display visit form

    If request method is 'GET', display form for making appointment
    If request method is 'POST', write data to the database and redirect to user page
    """
    form = VisitForm()
    if form.validate_on_submit():
        visit = Visit(visit_date=str(form.visit_date.data),
                      visit_time=str(form.visit_time.data),
                      customer=current_user, hours=form.visit_time.data)
        db.session.add(visit)
        db.session.commit()
        flash(f'Wizyta umówiona {form.visit_date.data} na godzinę: {form.visit_time.data}.', category='success')
        return redirect(url_for('main.user', username=current_user.username))
    return render_template('main/visit.html', title='Umów wizytę', form=form)


@main.route('/user/visits/<username>')
@login_required
def user(username):
    """Display user profile page with user appointments

    If user is_admin is True, display visits of all users
    """
    user = User.query.filter_by(username=username).first_or_404()
    customers = User.query.all()
    if user != current_user:
        flash('Brak dostępu!', category='warning')
        return redirect(url_for('main.user', username=current_user.username))
    if user.is_admin:
        visits = Visit.query.all()
    else:
        visits = Visit.query.filter_by(user_id=user.id)

    return render_template('main/user.html', user=user, visits=visits, customers=customers)

@main.route('/user/visits/delete/<visit>')
@login_required
def delete_visit(visit):
    """Deletes chosen visit

    If user id of given visit is not current_user id denies deleting this visit
    """
    item = Visit.query.filter_by(id=visit).first_or_404()
    item_owner = User.query.filter_by(id=item.user_id).first_or_404()
    if current_user.is_admin or item_owner == current_user:
        db.session.delete(item)
        db.session.commit()
        flash('Anulowano wizytę', category='success')
        return redirect(url_for('main.user', username=current_user.username))
    else:
        flash('Brak autoryzacji!', category='warning')
        return redirect(url_for('main.user', username=current_user.username))

