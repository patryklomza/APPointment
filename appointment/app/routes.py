from app import app
from flask import render_template, url_for, flash, redirect
from app.forms import LoginForm, VisitForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for user {form.username.data}, \
            remember_me={form.remember_me.data}')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/visit', methods=['GET','POST'])
def visit():
    form = VisitForm()

    return render_template('visit.html', title='Umów wizytę', form=form)
