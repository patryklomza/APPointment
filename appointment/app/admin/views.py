from . import admin
from app.decorators import admin_required
from flask import render_template


# all routes for admin are accessed with /admin prefix

@admin.route('/dashboard')
@admin_required
def admin_dashboard():
    return render_template('admin/admin_dashboard.html')
