from flask import Blueprint

from app.models import Permission

main = Blueprint('main', __name__)

# context processor adds Permission class to the template context
# this lets avoid  having to add a template argument in every render_template() call
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)

from . import views
