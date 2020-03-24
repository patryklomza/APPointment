from . import admin
from app.decorators import admin_required
from flask import render_template
from app.models import User


# all routes for admin are accessed with /admin prefix

@admin.route('/dashboard')
@admin_required
def admin_dashboard():
    return render_template('admin/admin_dashboard.html')


@admin.route('/users')
@admin_required
def users():
    registered_users = User.query.all()
    return render_template('admin/users.html', users=registered_users)
