from flask import render_template
from app.decorators import admin_required
from app.models import Visit, User
from . import admin

# all routes for admin are accessed with /admin prefix

@admin.route('/dashboard')
@admin_required
def admin_dashboard():
    return render_template('admin/admin_dashboard.html')

@admin.route('/visits')
@admin_required
def customer_visits():
    all_visits = Visit.query.join(Visit.customer).filter_by(role_id=1)
    return render_template('admin/all_visits.html', all_visits=all_visits)
