from flask import Blueprint

liquidacion_bp = Blueprint('liquidacion_de_persona_natural', __name__, template_folder='templates')

from . import routes
