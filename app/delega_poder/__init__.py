from flask import Blueprint

delega_bp = Blueprint('delega_poder', __name__, template_folder='templates')

from . import routes