from flask import Blueprint

diagrama_bp = Blueprint('diagrama', __name__, static_folder='static', template_folder='templates')

from . import routes