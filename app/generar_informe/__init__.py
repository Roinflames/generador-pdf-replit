from flask import Blueprint

generar_informe = Blueprint('generar_informe', __name__, template_folder='templates')

from . import routes


