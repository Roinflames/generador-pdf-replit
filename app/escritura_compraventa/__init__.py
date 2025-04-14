from flask import Blueprint

escritura_bp = Blueprint('escritura_compraventa', __name__, template_folder='templates')

from . import routes

